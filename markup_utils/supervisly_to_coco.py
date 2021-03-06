import json
import os

train_path = '/workspace/mounted_vol/dataset/train_supervisely/ann/'
val_path = '/workspace/mounted_vol/dataset/val_supervisely/ann/'


def mark(name, path):
    files = [x[:-9] for x in filter(lambda x: os.path.isfile(path + x), os.listdir(path))]
    files.sort()
    # files = [i for i in os.listdir(path)]
    images = []
    annotations = []
    categories = [{'id': 1, 'name': '1'},
                  {'id': 2, 'name': '2'},
                  {'id': 3, 'name': '3'},
                  {'id': 4, 'name': '4'}]

    id_image = 1
    id_ann = 1

    for i in files:
        with open(path + str(i) + '.png.json') as json_file:
            data = json.load(json_file)
            size = data['size']
            objects = data['objects']
            images.append(
                {'id': id_image, 'file_name': str(i) + '.png', 'width': size['width'], 'height': size['height']})

            for j in objects:
                p = j['points']
                e = p['exterior']
                x0 = e[0][0]
                y0 = e[0][1]

                w = e[1][0] - x0
                h = e[1][1] - y0

                ann = {
                    'id': id_ann,
                    'image_id': id_image,
                    'category_id': 10 if int(j['classTitle']) == 0 else int(j['classTitle']),
                    'area': 0,
                    'segmentation': [[]],
                    'iscrowd': 0,
                    'ignore': 0,
                    'bbox': [x0, y0, w, h]
                }
                annotations.append(ann)

            id_image += 1
            print(images)
            print(annotations)

    r = {'images': images, 'annotations': annotations, 'categories': categories}
    # r = json.dumps(r)
    with open(name + ".json", "w") as f:
        json.dump(r, f, indent=4, sort_keys=True)


mark('train', train_path)
mark('val', val_path)
