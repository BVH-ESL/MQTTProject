local file = assert(io.popen('top | grep mosquitto', 'r'))
local output = file:read('*all')
file:close()
print(output)
