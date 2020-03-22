# res = ['Irene Adler was here', 35,  24.798]
# print('{0[0]:{1}s} {0[1]:{2}d} {0[2]:{3}f}'.format(res, 10, 5, .2))

metric_val = "first year"
sort_metric = lambda x : 1
lhalf = (len(metric_val) + 2) // 2
rhalf = round(float(len(metric_val)) / 2)
#res = "{1:{0:{2}s}}".format(str(sort_metric("SAMPLE here")), lhalf, rhalf)
res1 = "{space:{space}d}".format(val=str(sort_metric("SAMPLE here")), space=lhalf)
#res2 = "{val:{val}s}".format(val=str(sort_metric("SAMPLE here")), space=lhalf)
#res3 = "{space:{val}d}".format(val=str(sort_metric("SAMPLE here")), space=lhalf)
res4 = "{val:{space}s}".format(val=str(sort_metric("SAMPLE here")), space=lhalf)
print("res1 : {" + str(res1) + "}")
#print("res2 : {" + str(res2) + "}")
#print("res3 : {" + str(res3) + "}")
print("res4 : {" + str(res4) + "}")

res5 = "{0:^{1}s}".format(str(sort_metric("SAMPLE here")), lhalf)
print("res5 : {" + str(res5) + "}")

res6 = "{val:^{lent}f}".format(val=sort_metric("SAMPLE here"), lent=len(metric_val))
print("res6 : {" + str(res6) + "}")


# value = "0:^{1}.2f".format(sort_metric(series)), len(metric_val)
# res = "|{0:^{1}s}".format(value, (len(metric_val) + 2))