```

            _ _                        _ _
   ___ ___ | | | __ _  __ _  ___      (_) |_
  / __/ _ \| | |/ _` |/ _` |/ _ \_____| | __|
 | (_| (_) | | | (_| | (_| |  __/_____| | |_
  \___\___/|_|_|\__,_|\__, |\___|     |_|\__|
                      |___/

v 0.1.0
Updated: 20210602-08:41:54
```
Written by: Hans Tremmel

# Use-case

Create a pdf collage of photos from a directory of photos. Create a shapefile that maps the photos to a location in ArcGIS.

# What

Will recurs through a folder, creating a key.yml file, an index of all photos in the directory.  The key.yml file would configure captions, add/remove photos from final product.

Will then generate a standard img.tex file, in latex. Latex can be customized to improve formatting as desired.

A shapefile.csv is also generated to list metadata including coordinates to be used for mapping photos to location and direction.

Lastly, the final PDF is produced.

# How

Only tested in a linux virtual machine.

1. Populate `src/imgs` directory with individual directories of folders.
2. Run `make images` to compile key.yml and imgs.tex.
3. (Optional) modify key.yml as needed with fancy captions or remove photos.
4. Run `make` to create a pdf.
5. Run `make view` to view your product in okular. If you don't have okular, modify the makefile for your pdf viewer of your choice.

# Requirements

- cmake
- okular, or any other PDF viewer.
- Python3
- Python modules, see requirements.txt files.
- latexmk

# TODO

| Status      | Task                                                 |
|-------------|------------------------------------------------------|
| In progress | Dockerize workflow for crossplatform.                |
| In progress | Create python executable to couple collage workflow. |
| queued      | Fix shapefile.csv to export directly to `.shp`       |

