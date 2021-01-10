from railroad import *

MY_STYLE = '''\
	svg.railroad-diagram {
		background-color:rgba(0,0,0,0);
	}
	svg.railroad-diagram path {
		stroke-width:3;
		stroke:black;
		fill:rgba(0,0,0,0);
	}
	svg.railroad-diagram text {
		font:bold 14px monospace;
		text-anchor:middle;
	}
	svg.railroad-diagram text.label{
		text-anchor:start;
	}
	svg.railroad-diagram text.comment{
		font:italic 12px monospace;
	}
	svg.railroad-diagram rect{
		stroke-width:3;
		stroke:black;
		fill:hsl(1,100%,72%);
	}
	svg.railroad-diagram rect.group-box {
		stroke: gray;
		stroke-dasharray: 10 5;
		fill: none;
	}
'''

def mk_diagram(name, nodes):
    return Diagram(Start('complex', name), nodes, type='complex', css=MY_STYLE)

def character_immediate():
    inner = Sequence(
		Terminal("'"),
		Choice(
			1,
			Sequence(
				Terminal('\\'),
				Choice(
					1,
					Sequence(
						Terminal('x'),
						NonTerminal('hex-digit'),
						NonTerminal('hex-digit')
					),
					HorizontalChoice(
						Terminal('n'),
						Terminal('r'),
						Terminal('\\'),
						Terminal('0')
					),
					HorizontalChoice(
						Terminal('t'),
						Terminal('v'),
						Terminal('e')
					),
				)
			),
			NonTerminal('ascii-character')
		),
		Terminal("'")
    )

    return mk_diagram('character-immediate', inner)

def character_constant():
    return character_immediate()

def nop_instruction():
	inner = Sequence(
		Terminal('nop')
	)

	return mk_diagram('nop-instruction', inner)

def code_line():
	inner = Choice(
		1,
		Sequence(
			Optional(
				Terminal('global')
			),
			NonTerminal('identifier'),
			Terminal(':'),
			NonTerminal('label-type')
		),
		Sequence(
			Optional(
				Terminal('unsafe')
			),
			NonTerminal('code-instruction')
		)
	)

	return mk_diagram('code-line', inner)

def data_section():
	inner = Sequence(
		Terminal('section'),
		Choice(
			1,
			Terminal('data'),
			Terminal('rodata'),
			Terminal('udata')
		),
		Terminal('{'),
		ZeroOrMore(
			Choice(
				1,
				Sequence(
					Optional(
						Terminal('global')
					),
					NonTerminal('identifier'),
					Terminal(':'),
					NonTerminal('constant-type')
				),
				NonTerminal('constant-value')
			)
		),
		Terminal('}')
	)

	return mk_diagram('data-section', inner)

def extern_data_section():
	inner = Sequence(
		Terminal('section'),
		Choice(
			0,
			Terminal('extern.data'),
			Terminal('extern.rodata')
		),
		Terminal('{'),
		ZeroOrMore(
			Sequence(
				Optional(
					Terminal('dyn')
				),
				NonTerminal('identifier'),
				Terminal(':'),
				NonTerminal('constant-type')
			)
		),
		Terminal('}')
	)

	return mk_diagram('extern.data-section', inner)

extern_data_section().writeSvg(sys.stdout.write)
