#code to plot the hit/miss tries, this task will be executed whenever response arrives
import matplotlib.pyplot as plt

hitsArray_X = [0.5, 1.5, 2.5, 3.5, 4.5]
hitsArray_Y = [1.5, 3.5, 0.5, 2.5, 4.5]
missArray_X = [1.5, 2.5, 3.5, 4.5, 5.5]
missArray_Y = [2.5, 4.5, 1.5, 3.5, 5.5]

def plotBattleGroundHitMissPlot(hitsArray_X, hitsArray_Y, missArray_X, missArray_Y):
    plt.plot(hitsArray_X, hitsArray_Y, 'x')  # 'o' specifies circle markers
    plt.plot(missArray_X, missArray_Y, 'o')
    #plt.xlabel('x-axis')
    #plt.ylabel('y-axis')
    plt.grid(True)
    plt.title('Hit(X) Vs Miss(O) Plot as Points')
    plt.show()

plotBattleGroundHitMissPlot(hitsArray_X, hitsArray_Y, missArray_X, missArray_Y)
