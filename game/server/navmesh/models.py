from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from game.server.leaflet import LeafletPoly, ShapelyUtil

if TYPE_CHECKING:
    from game import Game
    from game.navmesh import NavMesh


class NavMeshPolyJs(BaseModel):
    id: int
    poly: LeafletPoly
    threatened: bool

    class Config:
        title = "NavMeshPoly"


class NavMeshJs(BaseModel):
    polys: list[NavMeshPolyJs]

    class Config:
        title = "NavMesh"

    @staticmethod
    def from_navmesh(navmesh: NavMesh, game: Game) -> NavMeshJs:
        return NavMeshJs(
            polys=[
                NavMeshPolyJs(
                    id=p.ident,
                    poly=ShapelyUtil.poly_to_leaflet(p.poly, game.theater),
                    threatened=p.threatened,
                )
                for p in navmesh.polys
            ]
        )


class NavMeshSelectionUpdateJs(BaseModel):
    poly_ids: list[int]

    class Config:
        title = "NavMeshSelectionUpdate"


class NavMeshSelectionJs(BaseModel):
    blue: list[int]
    red: list[int]

    class Config:
        title = "NavMeshSelection"

    @staticmethod
    def from_game(game: Game) -> NavMeshSelectionJs:
        return NavMeshSelectionJs(
            blue=sorted(game.blue.aoo_navmesh_poly_ids),
            red=sorted(game.red.aoo_navmesh_poly_ids),
        )


class NavMeshesJs(BaseModel):
    blue: NavMeshJs
    red: NavMeshJs

    class Config:
        title = "NavMeshes"

    @staticmethod
    def from_game(game: Game) -> NavMeshesJs:
        return NavMeshesJs(
            blue=NavMeshJs.from_navmesh(game.blue.nav_mesh, game),
            red=NavMeshJs.from_navmesh(game.red.nav_mesh, game),
        )
