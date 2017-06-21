import invert
import overlay
import preprocessing_image
import process_image

from datetime import datetime

# -------------------- Start Time --------------------

start_time = datetime.now()

# -------------------- Process Image --------------------

# Proses gambar dan cari bagian yang tidak bisa dilewati dan rencanakan jalur untuk dilewati

occupied_grids, planned_path = process_image.main('output/final.jpg')

# -------------------- Maze --------------------

print '\n========== Maze ==========\n'

# Tentukan ukuran maze yang diperlukan.

column_count = 0;
row_count = 0;

for occupied_grid in occupied_grids:
    if (column_count < occupied_grid[0]):
        column_count = occupied_grid[0]

    if (row_count < occupied_grid[1]):
        row_count = occupied_grid[1]

# Buat maze.

maze = [[' ' for x in xrange(row_count)] for y in xrange(column_count)]

# Isi bagian di maze yang tidak bisa dilewati.

for occupied_grid in occupied_grids:
    maze[occupied_grid[1] - 1][occupied_grid[0] - 1] = 'X'

# Isi awal dan akhir.

end_point = (20, 20)
start_point = (1, 1)

maze[end_point[1] - 1][end_point[0] - 1] = 'O'
maze[start_point[1] - 1][start_point[0] - 1] = 'O'

# Tampilkan maze.

for row in maze:
    print ''.join(row[column] for column in xrange(row_count))

# -------------------- Normal Step --------------------

print '\n========== Normal Step ==========\n'

previous_direction = 'Down'
previous_step = None

for step in planned_path.get(start_point)[1]:
    if (previous_step != None):
        if (previous_step[0] != step[0]):
            if (previous_step[0] < step[0]):
                if (previous_direction is 'Down'):
                    print 'Kiri'
                elif (previous_direction is 'Right'):
                    print 'Lurus'
                elif (previous_direction is 'Up'):
                    print 'Kanan'

                previous_direction = 'Right'
            else:
                if (previous_direction is 'Down'):
                    print 'Kanan'
                elif (previous_direction is 'Left'):
                    print 'Lurus'
                elif (previous_direction is 'Up'):
                    print 'Kiri'

                previous_direction = 'Left'
        else:
            if (previous_step[1] < step[1]):
                if (previous_direction is 'Down'):
                    print 'Lurus'
                elif (previous_direction is 'Left'):
                    print 'Kiri'
                elif (previous_direction is 'Right'):
                    print 'Kanan'

                previous_direction = 'Down'
            else:
                if (previous_direction is 'Left'):
                    print 'Kanan'
                elif (previous_direction is 'Right'):
                    print 'Kiri'
                elif (previous_direction is 'Up'):
                    print 'Lurus'

                previous_direction = 'Up'

    previous_step = step;

# -------------------- Simplified Step --------------------

print '\n========== Simplified Step ==========\n'

previous_direction = 'Down'
previous_possible_count = 0
previous_step = None;

for step in planned_path.get(start_point)[1]:
    if (previous_possible_count > 2):
        if (previous_step[0] != step[0]):
            if (previous_step[0] < step[0]):
                if (previous_direction is 'Down'):
                    print 'Kiri'
                elif (previous_direction is 'Right'):
                    print 'Lurus'
                elif (previous_direction is 'Up'):
                    print 'Kanan'
            else:
                if (previous_direction is 'Down'):
                    print 'Kanan'
                elif (previous_direction is 'Left'):
                    print 'Lurus'
                elif (previous_direction is 'Up'):
                    print 'Kiri'
        else:
            if (previous_step[1] < step[1]):
                if (previous_direction is 'Down'):
                    print 'Lurus'
                elif (previous_direction is 'Left'):
                    print 'Kiri'
                elif (previous_direction is 'Right'):
                    print 'Kanan'
            else:
                if (previous_direction is 'Left'):
                    print 'Kanan'
                elif (previous_direction is 'Right'):
                    print 'Kiri'
                elif (previous_direction is 'Up'):
                    print 'Lurus'

    if (previous_step != None):
        if (previous_step[0] != step[0]):
            if (previous_step[0] < step[0]):
                previous_direction = 'Right'
            else:
                previous_direction = 'Left'
        else:
            if (previous_step[1] < step[1]):
                previous_direction = 'Down'
            else:
                previous_direction = 'Up'

    previous_possible_count = 0

    if (step[1] - 2 >= 0 and maze[step[1] - 2][step[0] - 1] != 'X'):
        previous_possible_count += 1

    if (step[0] - 2 >= 0 and maze[step[1] - 1][step[0] - 2] != 'X'):
        previous_possible_count += 1

    if (step[0] < row_count and maze[step[1] - 1][step[0]] != 'X'):
        previous_possible_count += 1

    if (step[1] < column_count and maze[step[1]][step[0] - 1] != 'X'):
        previous_possible_count += 1

    previous_step = step;

# -------------------- Stop Time --------------------

end_time = datetime.now()

print '\nDuration: {}'.format(end_time - start_time)
