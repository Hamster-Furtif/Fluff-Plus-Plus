init
	import random
	var age = 20, height as H = 1.90, i, j
	const age2 = age*2
	var r = random.ranInt(1, 10)
	str name = "Hamster_Furtif", sprite as 6 = "$DOT$"
	const HP_index=1, mana_index = 2, max_HP=100, max_mana=20
	const line = "__________"
	lst stats = {max_HP, max_mana}
	const dimX=50, dimY = 60
	mat map = {dimX, dimY}
begin
	if (age == 20) then
		height = height*r
	endif
end