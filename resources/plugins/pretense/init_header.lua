

if lfs then
	local dir = lfs.writedir()..'Missions/Saves/'
	lfs.mkdir(dir)
	savefile = dir..savefile
	env.info('Pretense - Save file path: '..savefile)
end


do

