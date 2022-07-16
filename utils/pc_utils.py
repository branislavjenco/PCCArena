import os
import random
import logging
import numpy as np
import pandas as pd
import subprocess as sp
from typing import Union
from pathlib import Path
import numpy.typing as npt
# from pyntcloud import PyntCloud
#import open3d as o3d

logger = logging.getLogger(__name__)

def sample_from_mesh(
        mesh_file: Union[str, Path],
        src_dir: Union[str, Path],
        dest_dir: Union[str, Path],
        num_points: int,
        color: bool = False,
        display_id: int = 99
    ) -> None:
    # workaround for using xvfb along with multiprocess
    # ref:https://stackoverflow.com/a/41276014
    # Inject environment variable `DISPLAY`.
    env = dict(os.environ, DISPLAY=str(display_id))
    
    infile = Path(src_dir).joinpath(mesh_file)
    outfile = Path(dest_dir).joinpath(mesh_file).with_suffix('.ply')
    outfile.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        'cloudcompare.CloudCompare',
        '-SILENT',
        '-AUTO_SAVE', 'OFF',
        '-O', infile,
        '-SAMPLE_MESH', 'POINTS', str(num_points),
        '-CLEAR_MESHES',
        '-CLEAR_NORMALS'
    ]
    
    if color is False:
        cmd += [
            '-REMOVE_RGB'
        ]
    
    cmd += [
        '-C_EXPORT_FMT', 'PLY',
        '-NO_TIMESTAMP',
        '-SAVE_CLOUDS', 'FILE', outfile
    ]

    try:
        _ = sp.run(cmd, capture_output=True, text=True, env=env, check=True)
    except sp.CalledProcessError as e:
        logger.error(
            f"Error occurs when sampling {infile} to point cloud."
            "\n"
            f"Executed command: "
            "\n"
            f"{''.join(str(s)+' ' for s in cmd)}"
        )
        
        lines = [
            "===== stdout =====",
            f"{e.stdout}",
            "\n",
            "===== stderr =====",
            f"{e.stderr}",
        ]
        print('\n'.join(lines))
        
        raise e

def calculate_normal(
        pc_file: Union[str, Path],
        src_dir: Union[str, Path],
        dest_dir: Union[str, Path],
        knn: int,
        display_id: int = 99
    ) -> None:
    # workaround for using xvfb along with multiprocess
    # ref:https://stackoverflow.com/a/41276014
    # Inject environment variable `DISPLAY`.
    env = {
        **os.environ,
        "DISPLAY": str(display_id)
    }
    
    infile = Path(src_dir).joinpath(pc_file)
    outfile = Path(dest_dir).joinpath(pc_file).with_suffix('.ply')
    outfile.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        'xvfb-run',
        '-a',
        '/itf-fi-ml/home/branisj/CloudCompare/build/qCC/CloudCompare',
        '-SILENT',
        '-AUTO_SAVE', 'OFF',
        '-O', infile,
        '-OCTREE_NORMALS', 'auto',
        '-CLEAR_MESHES',
        '-ORIENT_NORMS_MST', str(knn),
        '-C_EXPORT_FMT', 'PLY',
        '-NO_TIMESTAMP',
        '-SAVE_CLOUDS', 'FILE', outfile
    ]
    
    try:
        _ = sp.run(cmd, capture_output=True, text=True, env=env, check=True)
    except sp.CalledProcessError as e:
        logger.error(
            f"Error occurs when calculating normals of {infile}."
            "\n"
            f"Executed command: "
            "\n"
            f"{''.join(str(s)+' ' for s in cmd)}"
        )
        
        lines = [
            "===== stdout =====",
            f"{e.stdout}",
            "\n",
            "===== stderr =====",
            f"{e.stderr}",
        ]
        print('\n'.join(lines))
        
        raise e
"""
def normalize(
        pc_file: Union[str, Path],
        src_dir: Union[str, Path],
        dest_dir: Union[str, Path],
        scale: int = 1
    ) -> None:
    infile = Path(src_dir).joinpath(pc_file)
    outfile = Path(dest_dir).joinpath(pc_file)
    outfile.parent.mkdir(parents=True, exist_ok=True)
    
    pc = o3d.io.read_point_cloud(str(infile))
    points = np.asarray(pc.points)
    points = points - np.min(points, axis=0)
    points = points / np.max(points) * scale
    pc.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud(outfile, pc)
"""
