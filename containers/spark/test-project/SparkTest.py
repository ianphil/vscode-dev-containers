import pyspark
sc = pyspark.SparkContext('local[*]')

txt = sc.textFile('file:////usr/share/doc/python3.7/copyright')
python_lines = txt.filter(lambda line: 'python' in line.lower())
print(f'\n\t Text count in copyright is: {txt.count()}\n')
print(f'\n\t Line count in copyright is: {python_lines.count()}\n')
