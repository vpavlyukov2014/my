

def signal_level_to_desc(level):
   if level <= 70:
       'level_5'
   elif level > 70 and level < 85:
       'level_4'
   elif  level > 86 and level < 100:
       'level_3'
   elif level > 100  and level < 110:
       'level_2'
   elif level >= 110:
       'level_1'


# if (x < -92)
# return 1
# else if (x > -21)
# return 100
# else
# return round((-0.0154*x*x)-(0.3794*x)+98.182)
