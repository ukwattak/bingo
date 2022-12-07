import loader as data
import numpy as np
import matplotlib.pyplot as plt

# Load draws from file
draws = data.draws('real', 'numbers.txt')
print("Total Draws :", len(draws))

# Load boards from file
board_shape = (5, 5)
boards = data.boards('real', 'boards.txt', board_shape)
print("Total boards loaded :", len(boards))

wining_draws = []
x = []  # X axis - Board Ids
scores = []

for board in boards:
    wining_draw = board.wining_draw(draws)
    wining_draws.append(wining_draw)
    scores.append(board.board_score(draws, wining_draw))
    x.append(board.id)

print("------------------ ")

print("Board to win last ", np.argmax(wining_draws))
print("The Board Score ", boards[np.argmax(wining_draws)].board_score(draws, np.max(wining_draws)))
boards[np.argmax(wining_draws)].print(draws, np.max(wining_draws))
img_name_last = boards[np.argmax(wining_draws)].print_card(draws, np.max(wining_draws),
                                                           len(boards), 'Board to win last')
print("Wining Draw is", np.max(wining_draws))
print("------------------ ")

print("------------------ ")

print("Board to win first ", np.argmin(wining_draws))
print("The Board Score ", boards[np.argmin(wining_draws)].board_score(draws, np.min(wining_draws)))
boards[np.argmin(wining_draws)].print(draws, np.min(wining_draws))
img_name_first = boards[np.argmin(wining_draws)].print_card(draws, np.min(wining_draws),
                                                            len(boards), 'Board to win first')
print("Wining Draw is", np.min(wining_draws))
print("------------------ ")


fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(18, 9))
gs = axs[0, 1].get_gridspec()
# remove the underlying axes
for ax in axs[0, :]:
    ax.remove()
ax_big = fig.add_subplot(gs[0, :])


image_last = plt.imread('output/board/'+img_name_last)
axs[1, 0].imshow(image_last)
axs[1, 0].get_xaxis().set_visible(False)
axs[1, 0].get_yaxis().set_visible(False)
image_first = plt.imread('output/board/'+img_name_first)
axs[1, 1].imshow(image_first)
axs[1, 1].get_xaxis().set_visible(False)
axs[1, 1].get_yaxis().set_visible(False)

ax2 = ax_big.twinx()
ax_big.plot(x, wining_draws, 'g-', label="Draws")
ax2.plot(x, scores, 'r-', label="Scores")

ax_big.set_xlabel('Boards')
ax_big.set_ylabel('Wining Draws', color='g')
ax2.set_ylabel('Wining Scores', color='r')

ax_big.annotate('Board to win first ('+str(np.argmin(wining_draws)+1)+')',
                xy=(np.argmin(wining_draws)+1, np.min(wining_draws)),
                xytext=(np.argmin(wining_draws)+5, np.min(wining_draws)-5),
                arrowprops=dict(facecolor='black', shrink=0.01)
                )

ax_big.annotate('Board to win last ('+str(np.argmax(wining_draws)+1)+')',
                xy=(np.argmax(wining_draws)+1, np.max(wining_draws)),
                xytext=(np.argmax(wining_draws)+5, np.max(wining_draws)+5),
                arrowprops=dict(facecolor='black', shrink=0.01)
                )

ax2.legend(loc='upper right')
ax_big.legend(loc='upper left')

fig.tight_layout()
plt.title("Comparison between wining score and number of draws to win")
plt.show()


#
# image = plt.imread('output/board/'+img_name_min)
# ax_board_min.imshow(image)
# ax2 = ax1.twinx()
# ax1.plot(x, wining_draws, 'g-', label="Draws")
# ax2.plot(x, scores, 'r-', label="Scores")
#
# ax1.set_xlabel('Boards')
# ax1.set_ylabel('Wining Draws', color='g')
# ax2.set_ylabel('Wining Scores', color='r')
#
# ax1.annotate('Board to win first ('+str(np.argmin(wining_draws)+1)+')',
#              xy=(np.argmin(wining_draws)+1, np.min(wining_draws)),
#              xytext=(np.argmin(wining_draws)+5, np.min(wining_draws)-5),
#              arrowprops=dict(facecolor='black', shrink=0.01),
#              )
#
# ax1.annotate('Board to win last ('+str(np.argmax(wining_draws)+1)+')',
#              xy=(np.argmax(wining_draws)+1, np.max(wining_draws)),
#              xytext=(np.argmax(wining_draws)+5, np.max(wining_draws)+5),
#              arrowprops=dict(facecolor='black', shrink=0.01),
#              )
#
# ax2.legend(loc='upper right')
# ax1.legend(loc='upper left')
#
# plt.title("Comparison between wining score and number of draws to win")
# plt.show()
