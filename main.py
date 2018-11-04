import config

def inFS(ttype, stype):
	fs = set()
	if stype in config.first_set.keys(): fs = config.first_set[stype]
	if stype in config.terminal: fs = set([stype])

	if ttype == 'line_num':
		return 'line_num' in fs or 'const' in fs
	return ttype in fs

stack = ['EOF', config.startSymbol]
rules = []
for key in config.grammar_rule.keys():
	for a in config.grammar_rule[key]: 
		rules.append(a)
def parsing(tokens, last_line = 0):
	print('Syntactic analysis')
	bcode = config.BCode()
	
	output = []
	position = 0
	prev_term_goto = 0
	prev_term_if = 0
	while len(stack) > 0 and ((last_line == 0 and position < len(tokens)) or last_line == 1):
		stype = stack.pop()
		token_type = tokens[position][0]
		token_value = tokens[position][1]

		print('stype', stype, 'token_type', token_type, 'token_value', token_value)
		if stype in config.terminal:
			if stype == token_type:
				position += 1
				print('pop', stype)
				if prev_term_goto and token_type == 'line_num':
					output.append(bcode.bcode_format['GOTO'].format(token_value))
					prev_term_goto = 0
				elif prev_term_if and token_type == 'line_num':
					output.append(bcode.bcode_format['GOTO'].format(token_value))
					prev_term_id = 0
				elif token_type == 'GOTO':
					prev_term_goto = 1
					continue
				else:
					if token_type == 'IF':
						prev_term_if = 1
					output.append(bcode.bcode_format[token_type].format(token_value))
				if token_type == 'EOF':
					print('input accepted')
			else:
				print('bad term on input:', token_type)
				break
		elif inFS(token_type, stype):
			rule = config.paring_table[stype][config.terminal.index(token_type)]
			if rule < 0:
				print ('Error in parsing')
				break
			print('rule', rule)
			for r in reversed(rules[rule]):
				print (r)
				stack.append(r)
		print('stack', stack)

	return ' '.join(output)


def scanner(line = ''):
	bcode = config.BCode()
	tok = line.split(' ')
	matcher =  bcode.GetMatcher()
	valid = []
	is_line_num = 0
	for i, t in enumerate(tok):
		tok = bcode.GetToken(i, t, is_line_num)
		if tok[0] == None:
			print ('Input invalid')
			return []
		# print (tok)
		valid.append(tok)
	if valid[-1][0] == 'const':
		if valid[-2][0] == 'GOTO' or (len(valid) > 5 and valid[-5][0] == 'IF'):
			valid[-1] = ('line_num', valid[-1][1])
	return valid

def main(file = 'input.txt'):
	output = ''
	tokens = []
	with open(file, 'r') as fd:
		for line in fd.readlines():
			tok = scanner(line.strip())
			tokens += tok
			# print (tok)
			output += parsing(tok) + '\n'
	# output += parsing(tokens)
	output += '0\n'
	print (output)
	with open('output.txt', 'w') as fd:
		fd.write(output)
	

if __name__ == '__main__':
	main()