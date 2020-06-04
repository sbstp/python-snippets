from format import f

bar = "HEY"
wicked = 5
foo = 3
x = f('foo {bar.lower()!r} {wicked+foo}')
print(x)
