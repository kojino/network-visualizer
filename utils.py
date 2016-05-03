import colorsys

def get_N_HexCol(N=5):
    HSV_tuples = [(0 + 1.2*x/N, 1, 0.7 - (0.7-0.588)*x/N) for x in xrange(N)]
    hex_out = []
    for rgb in HSV_tuples:
        rgb = map(lambda x: int(x*255),colorsys.hsv_to_rgb(*rgb))
        hex_out.append("".join(map(lambda x: chr(x).encode('hex'),rgb)))
    return hex_out

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
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
	  background-color: #c4ced3
	}
	td
	{
	  background-color: #c4ced3
	}
	table, th, td
	{
	  font-family:Arial, Helvetica, sans-serif;
	  border: 0px solid black;
	  text-align: right;
	}
	"""
	return css

#rgba(0, 0, 255, 0);
