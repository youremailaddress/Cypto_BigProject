from argparse import ArgumentParser
import os.path
import re
from math import sqrt,log10

dir_path = os.path.dirname(os.path.abspath(__file__))+'\\'

def get_html(rang,singledata,dobseries,triseries):
    dobymax = max(singledata)
    dobxrang = len(rang)-1
    dobxcat = rang
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>第一个 Highcharts 图表</title>
    </head>
    <body>
    <!-- 图表容器 DOM -->
    <div id="container1" style="width: 900px;height:900px;"></div>
    <div id="container2" style="width: 900px;height:900px;"></div>
    <div id="container3" style="width: 900px;height:900px;"></div>
    <!-- 引入 highcharts.js -->
    <script src="http://cdn.highcharts.com.cn/highcharts/highcharts.js"></script>
    <script src="http://code.jquery.com/jquery-1.8.3.min.js"></script>
    <script src="http://cdn.highcharts.com.cn/highcharts/highcharts-3d.js"></script>
    <script src="https://code.highcharts.com/modules/boost.js"></script>
    <script>
        // 图表配置
        var options = {
            chart: {
                type: 'line'
            },
            title: {
                text: '单字符统计'
            },
            xAxis: {
                categories: '''+str(rang)+'''
            },
            yAxis: {
                title: {
                    text: '频数'
                }
            },
            series: [{
                name: '',
                data: '''+str(singledata)+'''
            }],
        };
        var chart = Highcharts.chart('container1', options);
    </script>
    <script>
        $(function() {
	const chart = Highcharts.chart('container2', {
		chart: {
			type: 'column',
			options3d: {
				enabled: true,
				alpha: 20,
				beta: 30,
				depth: 400, // Set deph
				viewDistance: 2,
				frame: {
					bottom: {
						size: 1,
						color: 'rgba(0,0,255,0.05)'
					}
				}
			}
		},
		title: {
			text: '二字符统计'
		},
		subtitle: {
			text: ''
		},
		yAxis: {
			min: 0,
			max: '''+str(dobymax)+'''
		},
		xAxis: {
			min: 0,
			max: '''+str(dobxrang)+''',
			categories: '''+str(dobxcat)+''',
			gridLineWidth: 1
		},
		zAxis: {
			min: 0,
			max: '''+str(dobxrang)+''',
			categories: '''+str(dobxcat)+''',
			labels: {
				y: 10,
				rotation: 26
			}
		},
		plotOptions: {
			series: {
				groupZPadding: 10,
				depth: 400/'''+str(dobxrang)+''',
				groupPadding: 0,
				grouping: false,
			}
		},
		series: ['''+dobseries+''']
	});
	// Add mouse events for rotation
	$(chart.container).on('mousedown.hc touchstart.hc', function(eStart) {
		eStart = chart.pointer.normalize(eStart);
		var posX = eStart.pageX,
			posY = eStart.pageY,
			alpha = chart.options.chart.options3d.alpha,
			beta = chart.options.chart.options3d.beta,
			newAlpha,
			newBeta,
			sensitivity = 1; // lower is more sensitive
		$(document).on({
			'mousemove.hc touchdrag.hc': function(e) {
				// Run beta
				newBeta = beta + (posX - e.pageX) / sensitivity;
				chart.options.chart.options3d.beta = newBeta;
				// Run alpha
				newAlpha = alpha + (e.pageY - posY) / sensitivity;
				chart.options.chart.options3d.alpha = newAlpha;
				chart.redraw(false);
			},
			'mouseup touchend': function() {
				$(document).off('.hc');
			}
		});
	});
    });
    </script>
    <script>
    var chart = new Highcharts.Chart({
	chart: {
		renderTo: 'container3',
		margin: 100,
		type: 'scatter',
		options3d: {
			enabled: true,
			alpha: 10,
			beta: 30,
			depth: 400,
			viewDistance: 5,
			frame: {
				bottom: { size: 1, color: 'rgba(0,0,0,0.02)' },
				back: { size: 1, color: 'rgba(0,0,0,0.04)' },
				side: { size: 1, color: 'rgba(0,0,0,0.06)' }
			}
		}
	},
    boost: {
        useGPUTranslations: true
    },
	title: {
		text: '3D散点图'
	},
	subtitle: {
		text: '单击并拖动鼠标可旋转绘图区'
	},
    plotOptions: {
		scatter: {
			width: 10,
			height: 10,
			depth: 10
		},
		series:{
			turboThreshold:2000
		}
	},
	yAxis: {
		min: 0,
		max: '''+str(dobxrang)+''',
		title: null
	},
	xAxis: {
		min: 0,
		max: '''+str(dobxrang)+''',
		gridLineWidth: 1
	},
	zAxis: {
		min: 0,
		max: '''+str(dobxrang)+'''
	},
	legend: {
		enabled: false
	},
	series: ['''+triseries+''']
    });
    // Add mouse events for rotation
    $(chart.container).bind('mousedown.hc touchstart.hc', function (e) {
        e = chart.pointer.normalize(e);
        var posX = e.pageX,
            posY = e.pageY,
            alpha = chart.options.chart.options3d.alpha,
            beta = chart.options.chart.options3d.beta,
            newAlpha,
            newBeta,
            sensitivity = 5; // lower is more sensitive
        $(document).bind({
            'mousemove.hc touchdrag.hc': function (e) {
                // Run beta
                newBeta = beta + (posX - e.pageX) / sensitivity;
                newBeta = Math.min(100, Math.max(-100, newBeta));
                chart.options.chart.options3d.beta = newBeta;
                // Run alpha
                newAlpha = alpha + (e.pageY - posY) / sensitivity;
                newAlpha = Math.min(100, Math.max(-100, newAlpha));
                chart.options.chart.options3d.alpha = newAlpha;
                chart.redraw(false);
            },
            'mouseup touchend': function () {
                $(document).unbind('.hc');
            }
        });
    });
        </script>
    </body>
    </html>
    '''

def get_series(rang,lis):
    neww = []
    for i in rang:
        one = []
        if len(set(lis[rang.index(i)])) == 1:
            continue
        for j in rang:
            one.append((i,lis[rang.index(i)][rang.index(j)]))
        if i == 10 or i == ord("'"):
            neww.append("{\nstack: "+str(i)+",\nname:'"+str(i)+"',\ndata: "+str(one)+"}")
        else:
            neww.append("{\nstack: "+str(i)+",\nname:'"+chr(i)+"',\ndata: "+str(one)+"}")
    return ','.join(neww)

def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b

def rindex(mid,v):
    mid.reverse()
    return len(mid)-mid.index(v)

def get_series_3d(rang,mes,mid,v_min = 0):
    lis = []
    for (i,j,k,v) in mes:
        if v < v_min:
            continue
        # r,g,b = rgb(200000,200000*ave,min(200000*ave,2000*v))
        r,g,b = rgb(0,len(mid),(mid.index(v)+2*rindex(mid.copy(),v))/3)
        if rang[i] < 31 or rang[i] == ord("'") or rang[j] <31 or rang[j] == ord("'") or rang[k] <31 or rang[k] == ord("'"):
            lis.append("{\nname: '"+str(rang[i])+str(rang[j])+str(rang[k])+":"+str(v)+"',\ndata: [["+str(i)+","+str(j)+","+str(k)+"]],\ncolor:{\nradialGradient: { cx: 0.4, cy: 0.3, r: 0.5 },\nstops: [\n[0, 'white'],\n[1,'rgb("+str(r)+","+str(g)+","+str(b)+")']\n]\n},\nmarker:{\nradius:3\n}\n}")
        else:
            lis.append("{\nname: '"+chr(rang[i])+chr(rang[j])+chr(rang[k])+":"+str(v)+"',\ndata: [["+str(i)+","+str(j)+","+str(k)+"]],\ncolor:{\nradialGradient: { cx: 0.4, cy: 0.3, r: 0.5 },\nstops: [\n[0, 'white'],\n[1,'rgb("+str(r)+","+str(g)+","+str(b)+")']\n]\n},\nmarker:{\nradius:3\n}\n}")
    return ",".join(lis)

def analysis(rang,anadir,htmldir,v_min):
    if os.path.exists(dir_path+htmldir) == True:
        print("[warning]path exist.Overwritting")
    with open(dir_path+anadir,"r",encoding='utf-8') as g:
        if rang == '':
            single = [0]*128
            c = g.read(1)
            while c != '':
                single[ord(c)] += 1
                c = g.read(1)
            rang = []
            singledata = []
            for i in range(128):
                if single[i]!=0:
                    rang.append(i)
                    singledata.append(single[i])
            g.seek(0,0)
            transfer = [[0 for i in range(128)] for j in range(128)]
            c = g.read(2)
            while len(c) == 2:
                transfer[ord(c[0])][ord(c[1])] += 1
                c = g.read(2)
            g.seek(1,0)
            c = g.read(2)
            while len(c) == 2:
                transfer[ord(c[0])][ord(c[1])] += 1
                c = g.read(2)
            tran_2d = [[0 for j in rang] for i in rang]
            for i in range(128):
                for j in range(128):
                    if transfer[i][j] != 0:
                        tran_2d[rang.index(j)][rang.index(i)] = transfer[i][j]
            g.seek(0,0)
            transfer3d = [[[0 for i in range(128)] for j in range(128)] for k in range(128)]
            c = g.read(3)
            while len(c) == 3:
                transfer3d[ord(c[0])][ord(c[1])][ord(c[2])] += 1
                c = g.read(3)
            g.seek(1,0)
            c = g.read(3)
            while len(c) == 3:
                transfer3d[ord(c[0])][ord(c[1])][ord(c[2])] += 1
                c = g.read(3)
            g.seek(2,0)
            c = g.read(3)
            while len(c) == 3:
                transfer3d[ord(c[0])][ord(c[1])][ord(c[2])] += 1
                c = g.read(3)
            mes = []
            mid = []
            for i in range(128):
                for j in range(128):
                    for k in range(128):
                        if transfer3d[i][j][k]>=int(v_min):
                            mid.append(transfer3d[i][j][k])
                            mes.append((rang.index(i),rang.index(j),rang.index(k),transfer3d[i][j][k]))
            mid.sort()
            
        else:
            single = [0]*len(rang)
            c = g.read(1)
            while c != '':
                if c in rang:
                    single[rang.index(c)] += 1
                c = g.read(1)
            singledata = single
            g.seek(0,0)
            transfer = [[0 for i in range(len(rang))] for j in range(len(rang))]
            c = g.read(2)
            while len(c) == 2:
                if c[0] in rang and c[1] in rang:
                    transfer[rang.index(c[0])][rang.index(c[1])] += 1
                c = g.read(2)
            g.seek(1,0)
            c = g.read(2)
            while len(c) == 2:
                if c[0] in rang and c[1] in rang:
                    transfer[rang.index(c[0])][rang.index(c[1])] += 1
                c = g.read(2)
            tran_2d = transfer
    
            g.seek(0,0)
            transfer3d = [[[0 for i in rang] for j in rang] for k in rang]
            c = g.read(3)
            while len(c) == 3:
                if c[0] in rang and c[1] in rang and c[2] in rang:
                    transfer3d[rang.index(c[0])][rang.index(c[1])][rang.index(c[2])] += 1
                c = g.read(3)
            g.seek(1,0)
            c = g.read(3)
            while len(c) == 3:
                if c[0] in rang and c[1] in rang and c[2] in rang:
                    transfer3d[rang.index(c[0])][rang.index(c[1])][rang.index(c[2])] += 1
                c = g.read(3)
            g.seek(2,0)
            c = g.read(3)
            while len(c) == 3:
                if c[0] in rang and c[1] in rang and c[2] in rang:
                    transfer3d[rang.index(c[0])][rang.index(c[1])][rang.index(c[2])] += 1
                c = g.read(3)
            mes = []
            mid = []
            for i in rang:
                for j in rang:
                    for k in rang:
                        if transfer3d[rang.index(i)][rang.index(j)][rang.index(k)]>=int(v_min):
                            mid.append(transfer3d[rang.index(i)][rang.index(j)][rang.index(k)])
                        mes.append((rang.index(i),rang.index(j),rang.index(k),transfer3d[rang.index(i)][rang.index(j)][rang.index(k)]))
            mid.sort()
            rang = [ord(i) for i in rang]
    with open(dir_path+htmldir,"w",encoding="utf-8") as f:
        f.write(get_html(["%c(%d)"%(i,i) for i in rang],singledata,get_series(rang,tran_2d),get_series_3d(rang,mes,mid,int(v_min))))

def prepare(anadir,predir):
    if os.path.exists(dir_path+predir) == True:
        print("[warning]path exist.Overwritting")
    f = open(dir_path+anadir,"r",encoding="utf-8",errors="ignore")
    g = open(dir_path+predir,"w",encoding="utf-8")
    c = f.read(1)
    while c!='':
        if 65<=ord(c)<=90:
            g.write(chr(ord(c)+32))
            c = f.read(1)
        if 97<=ord(c)<=122:
            g.write(c)
            c = f.read(1)
        else:
            c = f.read(1)
            continue
    f.close()
    g.close()

def encrypt(paswd,anadir,encrydir):
    if os.path.exists(dir_path+encrydir) == True:
        print("[warning]path exist.Overwritting")
    f = open(dir_path+anadir,"r",encoding="utf-8")
    g = open(dir_path+encrydir,"w",encoding="utf-8")
    c = f.read(1)
    t = 0
    le = len(paswd)
    while c!='':
        g.write(chr((ord(c)+ord(paswd[t%le])-194)%26+97))
        c = f.read(1)
        t += 1
    f.close()
    g.close()

def decrypt(paswd,encrydir,anadir):
    if os.path.exists(dir_path+anadir) == True:
        print("[warning]path exist.Overwritting")
    f = open(dir_path+encrydir,"r",encoding="utf-8")
    g = open(dir_path+anadir,"w",encoding="utf-8")
    c = f.read(1)
    t = 0
    le = len(paswd)
    while c!='':
        g.write(chr((ord(c)-ord(paswd[t%le]))%26+97))
        c = f.read(1)
        t += 1
    f.close()
    g.close()

def get_max_index(encrydir,num):
    rang="qwertyuiopasdfghjklzxcvbnm"
    g = open(dir_path+encrydir,"r")
    g.seek(0,0)
    transfer3d = [[[0 for i in rang] for j in rang] for k in rang]
    c = g.read(3)
    while len(c) == 3:
        if c[0] in rang and c[1] in rang and c[2] in rang:
            transfer3d[rang.index(c[0])][rang.index(c[1])][rang.index(c[2])] += 1
        c = g.read(3)
    g.seek(1,0)
    c = g.read(3)
    while len(c) == 3:
        if c[0] in rang and c[1] in rang and c[2] in rang:
            transfer3d[rang.index(c[0])][rang.index(c[1])][rang.index(c[2])] += 1
        c = g.read(3)
    g.seek(2,0)
    c = g.read(3)
    while len(c) == 3:
        if c[0] in rang and c[1] in rang and c[2] in rang:
            transfer3d[rang.index(c[0])][rang.index(c[1])][rang.index(c[2])] += 1
        c = g.read(3)
    mes = []
    for i in rang:
        for j in rang:
            for k in rang:
                if transfer3d[rang.index(i)][rang.index(j)][rang.index(k)]>=num:
                    mes.append((transfer3d[rang.index(i)][rang.index(j)][rang.index(k)],rang.index(i),rang.index(j),rang.index(k)))
    mes.sort(reverse=True)
    if len(mes) == 0:
        print("[fatal]No Enough data")
        exit()
    ret = []
    t = 0
    for i in mes:
        ret.append((rang[i[1]]+rang[i[2]]+rang[i[3]],i[0]))
        t += i[0]
        if t > 5000:
            return ret
    return [(rang[i[1]]+rang[i[2]]+rang[i[3]],i[0]) for i in mes]

def Kasiski(encrydir):
    with open(dir_path+encrydir,"r",encoding="utf-8") as f:
        c = f.read()
        if len(c) < 100:
            print("[fatal]No Enough data")
            exit()
        b = []

        mm = get_max_index(encrydir,len(c)/10000)

        for tex,num in mm:
            t = c.find(tex)
            all_index = [substr.start() for substr in re.finditer(c[t:t+3], c)]
            all_index = [all_index[i]-all_index[i-1] for i in range(1,len(all_index))]
            try:
                b.append([len([0 for i in all_index if not i%n]) for n in range(1,max(all_index)//2)])
            except ValueError:
                pass
        all = [0]*max([(len(i)) for i in b])
        for i in range(len(b)):
            for j in range(len(b[i])):
                all[j] += b[i][j]
        
        all = [all[i]**(1.5)*log10(i)/(all[i-1]+all[i]+all[i+1]+1) for i in range(1,len(all)-1)]
        # import matplotlib.pyplot as plt
        # plt.plot(range(1,len(all)+1),all)
        # plt.show()
        prob = [(all[i]/sum(all),i+2) for i in range(len(all))]
        prob.sort(reverse=True)
        print(prob[:10])

def mutiple(arr1,arr2):
    return sum([arr1[i]*arr2[i] for i in range(len(arr1))])

def out_k(pre_p,new_p):
    value = []
    new_p_standard_temp = [i**2 for i in new_p]
    new_p = [i/sqrt(sum(new_p_standard_temp)) for i in new_p]
    for i in range(26):
        value.append(mutiple(new_p,pre_p))
        a = new_p.pop()
        new_p.insert(0,a)
    if chr(123-value.index(max(value))) == "{":
        return 'a'
    else:
        return chr(123-value.index(max(value)))
    
def guess_de(encrydir,anadir,lenpw):
    lenpw = int(lenpw)
    pre_p = [0.3191191362182518, 0.058298732856328105, 0.10870447373076729, 0.1661826480147208, 0.49632071363343133, 0.08705735710717093, 0.07873454873022864, 0.23811828285955997, 0.27219100072197155, 0.005978355313014879, 0.030165296089199264, 0.15727372637179668, 0.0940125678634889, 0.2637118954741008, 0.2933301525150503, 0.07537416600526603, 0.0037120506845517223, 0.23393734156222276, 0.24722257559114474, 0.35385611578210946, 0.10776669250519633, 0.03821458494201668, 0.0922151538478112, 0.0058611326598185095, 0.07713250580321158, 0.002891492112177131]
    new_p = [[0 for i in range(26)] for j in range(lenpw)]
    f = open(dir_path+encrydir,"r",encoding="utf-8")
    g = open(dir_path+anadir,"w",encoding="utf-8")
    c = f.read(1)
    t = 0
    while c!='':
        new_p[t%lenpw][ord(c)-97] += 1
        c = f.read(1)
        t += 1
    key = []
    
    for i in range(lenpw):
        for j in range(26):
            new_p[i][j] /= t
        key.append(out_k(pre_p,new_p[i]))
    print("Key likey to be "+"".join(key)+".")
    print("".join(key))
    decrypt(key,encrydir,anadir)
        
def main():
    parser = ArgumentParser(description="A Tool for Vigenere Cipher mode(Must):analysis,prepare,encrypt,Kasiski,decrypt,guess")
    parser.add_argument('-m','--mode', default='')
    parser.add_argument('-r','--range', default='')
    parser.add_argument('-a','--anadir', default='')
    parser.add_argument('-hd','--htmldir', default='output.html')
    parser.add_argument('-pd','--predir', default='prepared.txt')
    parser.add_argument('-ed','--encrydir', default='encry.txt')
    parser.add_argument('-pw','--paswd', default='')
    parser.add_argument('-l','--len',default='')
    parser.add_argument('-vm','--vmin',default='1')
    args = parser.parse_args()
    if args.mode == "analysis":
        analysis(args.range,args.anadir,args.htmldir,args.vmin)
    elif args.mode == "prepare":
        prepare(args.anadir,args.predir)
    elif args.mode == "encrypt":
        encrypt(args.paswd,args.anadir,args.encrydir)
    elif args.mode == "Kasiski":
        Kasiski(args.encrydir)
    elif args.mode == "decrypt":
        decrypt(args.paswd,args.encrydir,args.anadir)
    elif args.mode == "guess":
        guess_de(args.encrydir,args.anadir,args.len)
    else:
        raise Exception("ValueError","Invalid args mode!")

if __name__ == '__main__':
    main()

