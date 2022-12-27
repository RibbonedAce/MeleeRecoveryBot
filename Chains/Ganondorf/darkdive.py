from melee.enums import Character

from Chains.Abstract import ElementalDive
from Utils import Trajectory, TrajectoryFrame as TF, Vector2 as V2
from Utils.enums import LEDGE_GRAB_MODE


class DarkDive(ElementalDive):
    TRAJECTORY = Trajectory(Character.GANONDORF, 0, 44, LEDGE_GRAB_MODE.ALWAYS, False, [
        TF.fixed(V2.zero(), V2(6.82229, 3.00536)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.044, -0.044, 0.044, 0, -0.044), 0), V2(3.41854, 4.17136)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.088, -0.088, 0.088, 0, -0.088), 0), V2(2.97136, 4.52726)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.132, -0.132, 0.132, 0, -0.132), 0), V2(9.48408, 4.00385)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.176, -0.176, 0.176, 0, -0.176), 0), V2(10.68512, 1.69978)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04187, -0.04613, 0.21787, -0.00213, -0.22213), -0.00087), V2(10.71249, 1.55549)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04096, -0.04704, 0.25883, -0.00517, -0.26917), -0.0021), V2(10.73668, 1.46099)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04279, -0.04521, 0.30162, -0.00638, -0.31438), -0.0026), V2(10.75568, 1.41198)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04461, -0.04339, 0.34623, -0.00577, -0.35777), -0.00235), V2(10.76583, 1.4042)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04643, -0.04157, 0.39266, -0.00334, -0.39934), -0.00136), V2(10.76215, 1.43336)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04825, -0.03975, 0.44091, 0.00091, -0.43909), 0.00037), V2(10.73588, 1.4952)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.05008, -0.03792, 0.49099, 0.00699, -0.47701), 0.00284), V2(10.68268, 1.58543)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.0519, -0.28549, 0.54289, 0.01489, -0.45646), 0.00606), V2(10.59043, 1.69978)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.41638, 0.32838, 0.95927, 0.38727, -0.12808), 2.84533), V2(4.28408, 1.69978)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04786, -0.04014, 1.00713, 0.39113, -0.16822), 2.73491), V2(3.17785, 1.69978)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04774, -0.04026, 1.05487, 0.39487, -0.20848), 2.6256), V2(3.7863, 1.69978)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04762, -0.04038, 1.06149, 0.39849, -0.24886), 2.51742), V2(3.80862, 1.69978)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.0475, -0.0405, 1.06499, 0.40199, -0.26101), 2.41035), V2(3.81985, 2.33026)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04737, -0.04063, 1.06836, 0.40536, -0.25764), 2.30441), V2(3.82517, 2.26294)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04724, -0.04076, 1.0716, 0.4086, -0.2544), 2.19959), V2(3.82999, 2.13864)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04712, -0.04088, 1.07472, 0.41172, -0.25128), 2.09588), V2(3.83962, 2.01963)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.047, -0.041, 1.07772, 0.41472, -0.24828), 1.99331), V2(3.85875, 1.96821)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04687, -0.04113, 1.08059, 0.41759, -0.24541), 1.89185), V2(3.89097, 2.04651)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04675, -0.04125, 1.08334, 0.42034, -0.24266), 1.79151), V2(4.19507, 2.31339)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04663, -0.04137, 1.08597, 0.42297, -0.24003), 1.69229), V2(4.55337, 2.69658)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.0465, -0.0415, 1.08847, 0.42547, -0.23753), 1.5942), V2(4.77227, 3.16121)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04637, -0.04163, 1.09084, 0.42784, -0.23516), 1.49722), V2(4.98158, 3.66881)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04625, -0.04175, 1.09309, 0.43009, -0.23291), 1.40436), V2(4.86576, 4.16086)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04613, -0.04187, 1.09522, 0.43222, -0.23078), 1.30663), V2(4.93086, 4.59776)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04601, -0.04199, 1.09723, 0.43423, -0.22877), 1.21302), V2(10.13076, 4.9876)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04587, -0.04213, 1.0991, 0.4361, -0.2269), 1.12053), V2(10.06803, 5.33732)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04576, -0.04224, 1.10086, 0.43786, -0.22514), 1.02916), V2(4.16913, 5.49883)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04563, -0.04237, 1.10249, 0.43949, -0.22351), 0.93891), V2(3.37916, 5.7875)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04551, -0.04249, 1.104, 0.441, -0.222), 0.84977), V2(4.205, 6.50863)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04538, -0.04262, 1.10538, 0.44238, -0.22062), 0.76177), V2(11.39693, 7.31673)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04526, -0.04274, 1.10664, 0.44364, -0.21936), 0.67488), V2(11.80814, 7.8722)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04514, -0.04286, 1.10778, 0.44478, -0.21822), 0.58912), V2(11.40607, 8.02565)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04501, -0.04299, 1.10879, 0.44579, -0.21721), 0.50447), V2(10.30527, 8.5079)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04488, -0.04312, 1.10967, 0.44667, -0.21633), 0.42094), V2(4.33091, 9.3997)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04477, -0.04323, 1.11044, 0.44744, -0.21556), 0.33854), V2(3.72317, 9.85487)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04463, -0.04337, 1.11107, 0.44807, -0.21493), 0.25727), V2(3.6623, 10.42325)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04452, -0.04348, 1.11159, 0.44859, -0.21441), 0.17709), V2(4.05747, 11.66661)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04438, -0.04362, 1.11197, 0.44897, -0.21403), 0.09805), V2(3.42157, 13.63853)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04427, -0.04373, 1.11224, 0.44924, -0.21376), 0.02013), V2(3.33973, 13.97571)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04414, -0.04386, 1.11238, 0.44938, -0.21362), -0.05665), V2(4.77655, 13.80859)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.08128, -0.04398, 1.1124, 0.4494, -0.2136), -0.13234), V2(6.38091, 14.22937)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04389, -0.04411, 1.11229, 0.44929, -0.21371), -0.30244), V2(6.68967, 14.82293)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04377, -0.04423, 1.11206, 0.44906, -0.21394), -0.55295), V2(6.38539, 15.64799)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04364, -0.04436, 1.1117, 0.4487, -0.2143), -0.78135), V2(5.97937, 14.53217)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04352, -0.04448, 1.11122, 0.44822, -0.21478), -0.98763), V2(7.01775, 12.67262)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.0434, -0.0446, 1.11062, 0.44762, -0.21538), -1.17178), V2(4.02711, 10.69318)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04326, -0.04474, 1.10988, 0.44688, -0.21612), -1.33383), V2(2.6437, 8.2338)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04316, -0.04484, 1.10904, 0.44604, -0.21696), -1.47376), V2(2, 6.82758)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04302, -0.04498, 1.10806, 0.44506, -0.21794), -1.59156), V2(2.58889, 6.67253)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.0429, -0.0451, 1.10696, 0.44396, -0.21904), -1.68725), V2(2.94444, 8.3987)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04277, -0.04523, 1.10573, 0.44273, -0.22027), -1.76082), V2(3.45689, 10.02879)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04266, -0.04534, 1.10439, 0.44139, -0.22161), -1.81227), V2(2.86595, 12.82765)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04252, -0.04548, 1.10291, 0.43991, -0.22309), -1.8416), V2(3.66016, 12.94481)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.0424, -0.0456, 1.10131, 0.43831, -0.22469), -1.84882), V2(3.81384, 11.99182)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04228, -0.04572, 1.09959, 0.43659, -0.22641), -1.83392), V2(2.98728, 10.8401)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04216, -0.04584, 1.09775, 0.43475, -0.22825), -1.7969), V2(3.07188, 8.58006)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04202, -0.04598, 1.09577, 0.43277, -0.23023), -1.73776), V2(3.04584, 6.23389)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04192, -0.04608, 1.09369, 0.43069, -0.23231), -1.6565), V2(3.11685, 4.57366)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04177, -0.04623, 1.09146, 0.42846, -0.23454), -1.55313), V2(3.85152, 2.90939)),
        TF.drift(Character.GANONDORF)
    ])

    REVERSE_TRAJECTORY = Trajectory(Character.GANONDORF, 0, 44, LEDGE_GRAB_MODE.DURING, False, [
        TF.fixed(V2.zero(), V2(6.82229, 3.00536)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.044, -0.044, 0.044, 0, -0.044), 0), V2(3.41854, 4.17136)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.088, -0.088, 0.088, 0, -0.088), 0), V2(2.97136, 4.52726)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.132, -0.132, 0.132, 0, -0.132), 0), V2(9.48408, 4.00385)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.176, -0.176, 0.176, 0, -0.176), 0), V2(10.68512, 1.69978)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04187, -0.04613, 0.21787, -0.00213, -0.22213), -0.00087), V2(10.71249, 1.55549)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04096, -0.04704, 0.25883, -0.00517, -0.26917), -0.0021), V2(10.73668, 1.46099)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04279, -0.04521, 0.30162, -0.00638, -0.31438), -0.0026), V2(10.75568, 1.41198)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04461, -0.04339, 0.34623, -0.00577, -0.35777), -0.00235), V2(10.76583, 1.4042)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04643, -0.04157, 0.39266, -0.00334, -0.39934), -0.00136), V2(10.76215, 1.43336)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04825, -0.03975, 0.44091, 0.00091, -0.43909), 0.00037), V2(10.73588, 1.4952)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.05008, -0.03792, 0.49099, 0.00699, -0.47701), 0.00284), V2(10.68268, 1.58543)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, -0.03453, -0.06588, 0.45646, None, -0.54289), 0.00606), V2(4.22097, 1.69978)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, -0.32838, -0.41638, 0.12808, -0.38727, -0.95927), 2.84533), V2(4.28408, 1.69978)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04014, -0.04786, 0.16822, -0.39113, -1.00713), 2.73491), V2(3.17785, 1.69978)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04026, -0.04774, 0.20848, -0.39487, -1.05487), 2.6256), V2(3.7863, 1.69978)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04038, -0.04762, 0.24886, -0.39849, -1.06149), 2.51742), V2(3.80862, 1.69978)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.0405, -0.0475, 0.26101, -0.40199, -1.06499), 2.41035), V2(3.81985, 2.33026)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04063, -0.04737, 0.25764, -0.40536, -1.06836), 2.30441), V2(3.82517, 2.26294)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04076, -0.04724, 0.2544, -0.4086, -1.0716), 2.19959), V2(3.82999, 2.13864)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04088, -0.04712, 0.25128, -0.41172, -1.07472), 2.09588), V2(3.83962, 2.01963)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.041, -0.047, 0.24828, -0.41472, -1.07772), 1.99331), V2(3.85875, 1.96821)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04113, -0.04687, 0.24541, -0.41759, -1.08059), 1.89185), V2(3.89097, 2.04651)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04125, -0.04675, 0.24266, -0.42034, -1.08334), 1.79151), V2(4.19507, 2.31339)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04137, -0.04663, 0.24003, -0.42297, -1.08597), 1.69229), V2(4.55337, 2.69658)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.0415, -0.0465, 0.23753, -0.42547, -1.08847), 1.5942), V2(4.77227, 3.16121)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04163, -0.04637, 0.23516, -0.42784, -1.09084), 1.49722), V2(4.98158, 3.66881)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04175, -0.04625, 0.23291, -0.43009, -1.09309), 1.40436), V2(4.86576, 4.16086)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04187, -0.04613, 0.23078, -0.43222, -1.09522), 1.30663), V2(4.93086, 4.59776)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04199, -0.04601, 0.22877, -0.43423, -1.09723), 1.21302), V2(2, 4.9876)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04213, -0.04587, 0.2269, -0.4361, -1.0991), 1.12053), V2(2, 5.33732)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04224, -0.04576, 0.22514, -0.43786, -1.10086), 1.02916), V2(4.16913, 5.49883)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04237, -0.04563, 0.22351, -0.43949, -1.10249), 0.93891), V2(3.37916, 5.7875)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04249, -0.04551, 0.222, -0.441, -1.104), 0.84977), V2(4.205, 6.50863)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04262, -0.04538, 0.22062, -0.44238, -1.10538), 0.76177), V2(2, 7.31673)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04274, -0.04526, 0.21936, -0.44364, -1.10664), 0.67488), V2(2, 7.8722)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04286, -0.04514, 0.21822, -0.44478, -1.10778), 0.58912), V2(2, 8.02565)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04299, -0.04501, 0.21721, -0.44579, -1.10879), 0.50447), V2(2, 8.5079)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04312, -0.04488, 0.21633, -0.44667, -1.10967), 0.42094), V2(4.33091, 9.3997)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04323, -0.04477, 0.21556, -0.44744, -1.11044), 0.33854), V2(3.72317, 9.85487)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04337, -0.04463, 0.21493, -0.44807, -1.11107), 0.25727), V2(3.6623, 10.42325)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04348, -0.04452, 0.21441, -0.44859, -1.11159), 0.17709), V2(4.05747, 11.66661)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04362, -0.04438, 0.21403, -0.44897, -1.11197), 0.09805), V2(3.42157, 13.63853)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04373, -0.04427, 0.21376, -0.44924, -1.11224), 0.02013), V2(3.33973, 13.97571)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04386, -0.04414, 0.21362, -0.44938, -1.11238), -0.05665), V2(4.77655, 13.80859)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04398, -0.08128, 0.2136, -0.4494, -1.1124), -0.13234), V2(4.04944, 14.22937)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04411, -0.04389, 0.21371, -0.44929, -1.11229), -0.30244), V2(5.16347, 14.82293)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04423, -0.04377, 0.21394, -0.44906, -1.11206), -0.55295), V2(6.22149, 15.64799)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04436, -0.04364, 0.2143, -0.4487, -1.1117), -0.78135), V2(6.50696, 14.53217)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04448, -0.04352, 0.21478, -0.44822, -1.11122), -0.98763), V2(5.79451, 12.67262)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.0446, -0.0434, 0.21538, -0.44762, -1.11062), -1.17178), V2(4.02711, 10.69318)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04474, -0.04326, 0.21612, -0.44688, -1.10988), -1.33383), V2(2.6437, 8.2338)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04484, -0.04316, 0.21696, -0.44604, -1.10904), -1.47376), V2(2, 6.82758)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04498, -0.04302, 0.21794, -0.44506, -1.10806), -1.59156), V2(2.58889, 6.67253)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.0451, -0.0429, 0.21904, -0.44396, -1.10696), -1.68725), V2(2.94444, 8.3987)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04523, -0.04277, 0.22027, -0.44273, -1.10573), -1.76082), V2(3.45689, 10.02879)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04534, -0.04266, 0.22161, -0.44139, -1.10439), -1.81227), V2(2.86595, 12.82765)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04548, -0.04252, 0.22309, -0.43991, -1.10291), -1.8416), V2(3.66016, 12.94481)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.0456, -0.0424, 0.22469, -0.43831, -1.10131), -1.84882), V2(3.81384, 11.99182)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04572, -0.04228, 0.22641, -0.43659, -1.09959), -1.83392), V2(2.98728, 10.8401)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04584, -0.04216, 0.22825, -0.43475, -1.09775), -1.7969), V2(3.07188, 8.58006)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04598, -0.04202, 0.23023, -0.43277, -1.09577), -1.73776), V2(3.04584, 6.23389)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04608, -0.04192, 0.23231, -0.43069, -1.09369), -1.6565), V2(3.11685, 4.57366)),
        TF(lambda v, i: V2(TF.default_horizontal(v.x, i.x, 0.04623, -0.04177, 0.23454, -0.42846, -1.09146), -1.55313), V2(3.85152, 2.90939)),
        TF.drift(Character.GANONDORF)
    ])

    @classmethod
    def _get_normal_trajectory(cls):
        return cls.TRAJECTORY

    @classmethod
    def _get_reverse_trajectory(cls):
        return cls.REVERSE_TRAJECTORY