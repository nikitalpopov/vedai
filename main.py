# 1: car, 2:trucks, 4: tractors, 5: camping cars, 7: motorcycles, 8:buses, 9: vans, 10: others, 11: pickup, 23: boats , 201: Small Land Vehicles, 31: Large land Vehicles

import os
import pandas as pd


def update_annotations(filename):
	with open('/path/to/annotations/' + filename, 'r') as file:
		data = file.read()

		text = '\n'.join(' '.join(line.split()) for line in data.split('\n'))
		text.replace('\t', ' ')

		# print(text)
		output = open(filename, 'w')
		output.write(text)
		output.close()

		data = pd.read_csv(filename, sep=' ', index_col=None, header=None, names=['x_center', 'y_center', 'orientation', 'class', 'is_contained', 'is_occluded', 'corner1_x', 'corner2_x', 'corner3_x', 'corner4_x', 'corner1_y', 'corner2_y', 'corner3_y', 'corner4_y'])

		data['class'].replace(11, 3, inplace=True)
		data['class'].replace(23, 6, inplace=True)
		data['class'].replace(201, 11, inplace=True)
		data['class'].replace(31, 12, inplace=True)

		data['class'] = data['class'] - 1
		data['x_center_ratio'] = data['x_center'].astype(float) / 1024.
		data['y_center_ratio'] = data['y_center'].astype(float) / 1024.
		data['width_ratio'] = (data[['corner1_x', 'corner2_x', 'corner3_x', 'corner4_x']].max(axis=1) - data[['corner1_x', 'corner2_x', 'corner3_x', 'corner4_x']].min(axis=1)) / 1024.
		data['height_ratio'] = (data[['corner1_y', 'corner2_y', 'corner3_y', 'corner4_y']].max(axis=1) - data[['corner1_y', 'corner2_y', 'corner3_y', 'corner4_y']].min(axis=1)) / 1024.

		res = data.drop(['x_center', 'y_center', 'corner1_x', 'corner2_x', 'corner3_x', 'corner4_x', 'orientation', 'corner1_y', 'corner2_y', 'corner3_y', 'corner4_y', 'is_contained', 'is_occluded'], axis=1)
		# print(res)
		res.to_csv(filename, sep=' ', index=False, header=None)


list = os.listdir('/path/to/annotations/')
list.remove('.DS_Store')  # for macOS
for filename in list:
	# print(filename)
	update_annotations(filename)
