with open("vectors/input/la.txt", "r") as f:
    content = f.read()

content = (
    content.replace("v", "u").replace("j", "i").replace("V", "U").replace("J", "I")
)

with open("vectors/input/la.txt", "w") as f:
    f.write(content)
