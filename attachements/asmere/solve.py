import sys

def message(inst):

    i = 0
    args = []
    bracket = False
    while i < len(inst):
        c = inst[i]

        if c == '"':
            bracket = not bracket

        if bracket:
            arg_elt = { 'type':'bracket', 'data':'' }
            i += 1
            while i < len(inst) and inst[i] != '"':
                arg_elt['data'] += inst[i]
                i += 1
            i -= 1
            args.append(arg_elt)

        elif not bracket and c == '$':
            arg_elt = { 'type':'variable', 'data':'' }
            i += 1
            while i < len(inst) and inst[i] != ' ':
                arg_elt['data'] += inst[i]
                i += 1
            args.append(arg_elt)

        elif not bracket and c not in [' ','"','$']:
            arg_elt = { 'type':'no_bracket', 'data':'' }
            while i < len(inst) and inst[i] != ' ':
                arg_elt['data'] += inst[i]
                i += 1
            args.append(arg_elt)

        i += 1

    i = 0
    out = '' 
    while i < len(args):
        elt = args[i]
        
        if i == 0:
            if elt['type'] in ['bracket','no_bracket']:
                out += 'print("'+elt['data']
            elif elt['type'] == 'variable':
                out += 'print(str('+elt['data']+')'

        else:
            if elt['type'] == 'no_bracket':
                prev = args[i-1]
                if prev['type'] in ['bracket','no_bracket']:
                    out += ' '+elt['data']
                elif prev['type'] == 'variable':
                    out += '+" '+elt['data']

            if elt['type'] == 'bracket':
                prev = args[i-1]
                if prev['type'] == 'bracket':
                    out += elt['data']
                elif prev['type'] == 'no_bracket':
                    out += ' '+elt['data']
                elif prev['type'] == 'variable':
                    out += '+"'+elt['data']
            
            if elt['type'] == 'variable':
                prev = args[i-1]
                if prev['type'] == 'bracket':
                    out += '"+str('+elt['data']+')'
                elif prev['type'] == 'no_bracket':
                    out += ' "+str('+elt['data']+')'
                elif prev['type'] == 'variable':
                    out += ' "+str('+elt['data']+')'

        if i == (len(args)-1):
            if elt['type'] == 'variable':
                out += ')'
            else:
                out += '")'

        i += 1
    
    return out


def run():
    with open(sys.argv[1],'r') as f:
        code = f.read()

    instructions = code.splitlines()

    # remove comments
    instructions = [ inst for inst in instructions if len(inst) > 0 and inst[0] != ';' ]
    
    global_vars = []
    out = []
    for inst in instructions:
        inst = inst.split(' ')
    
        cmd = inst[0]
        if cmd == 'nombre':
            out += [f'{inst[1]} = {inst[2]}']
            global_vars += [inst[1]]
    
        elif cmd == 'incrementer':
            out += [f'{inst[1]} += {inst[2]}']
    
        elif cmd == 'message':
            out += [message(' '.join(inst[1:]))]

        elif cmd == 'appel':
            out += [inst[1]+'()']

        else:
            out += [' '.join(inst)]
    
    instructions = out
    

    # create functions
    out = []
    in_function = False
    for inst in instructions:
        if inst[-1] == ':' and inst[:3] != 'if ':
            out += [f'def {inst[:-1]}():']
            out += [ f'\tglobal {elt}' for elt in global_vars ]
            in_function = True
        elif in_function:
            if inst == 'retour':
                in_function = False
                out += ['\n']
            else:
                out += ['\t'+inst]
        else:
            out += [inst]
    instructions = out

    out = []
    global_inst = []
    for inst in instructions:
        if inst[:4] != 'def ' and inst[0] != '\t':
            global_inst += [inst]
        else:
            out += [inst]
    instructions = out + global_inst

    out = []
    in_if = 0 
    for inst in instructions:
        if inst.replace('\t','')[:3] == 'si ':
            out += ['\t'*in_if+inst.replace('si','if',1).replace('$','')+':']
            in_if += 1 
        elif in_if:
            if inst.replace('\t','') == 'finsi':
                in_if -= 1 
            else:
                out += ['\t'*in_if+inst]
        else:
            out += [inst]
    instructions = out

    instructions = '\n'.join(instructions)
    return instructions


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 " + sys.argv[0] + " <filename>")
        sys.exit(1)


main()
exec(run())
