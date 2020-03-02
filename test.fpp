init
	import sketch
	lst poly = {1+i(), 3+15*i(), 27+50*i(), 12+37*i()}
	var i
begin
	sketch.initWindow()
	sketch.drawRect(1, 3, 5, 6, null)
	sketch.drawPoly(poly, i, null)
	poly[1] = 5
end
