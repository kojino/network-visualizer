from colour import Color

def get_N_HexCol(N):
	hex_out = []
	first = Color("#c9e3a0")
	last = Color("#82bfd9")
	for i in list(first.range_to(last, N)):
		colorToAppend = i.hex
		if len(colorToAppend) == 4:
			colorToAppend = "#" + colorToAppend[1] + colorToAppend[1] + colorToAppend[2] + colorToAppend[2] + colorToAppend[3] + colorToAppend[3]
			print colorToAppend
			hex_out.append(colorToAppend)
		else:
			hex_out.append(colorToAppend)

	return hex_out

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

def CSSTableStyle():
	css = """
	table
	{
	  border-collapse: collapse;
	}
	th
	{
	  color: #000000;
	  background-color: #eaebeb
	}
	td
	{
	  background-color: #eaebeb
	}
	table, th, td
	{
	  font-family:Arial, Helvetica, sans-serif;
	  border: 0px solid black;
	  text-align: right;
	}
	"""
	return css
