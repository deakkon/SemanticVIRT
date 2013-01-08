formater = "%r %r %r %r "

print formater % (1,2,3,4)
print formater % ("one","two","three","four")
print formater % (True, False, False, True)
print formater % (formater,formater,formater,formater)
print formater % (
"I had this thing.",
"That you could type up right.",
"But it didn't sing.",
"So I said goodnight."
)