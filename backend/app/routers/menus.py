from uuid import UUID

from fastapi import APIRouter, File, Form, UploadFile, status

from app.deps import CurrentUser, MenuServiceDep
from app.exceptions import PayloadTooLarge, UnsupportedMedia
from app.schemas.dish import (
    ExplainDishRequest,
    ExplainDishResponse,
    MenuScanResponse,
    MenuScanSummary,
)

router = APIRouter(prefix="/menus", tags=["menus"])

_MAX_IMAGE_BYTES = 10 * 1024 * 1024
_ALLOWED_CONTENT_TYPES = frozenset(
    {"image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"}
)


@router.post("/scan", response_model=MenuScanResponse, status_code=status.HTTP_201_CREATED)
async def scan_menu(
    user: CurrentUser,
    menus: MenuServiceDep,
    image: UploadFile = File(...),
    target_language: str = Form(default=""),
    source_language: str = Form(default="auto"),
    restaurant_name: str | None = Form(default=None),
) -> MenuScanResponse:
    if image.content_type not in _ALLOWED_CONTENT_TYPES:
        raise UnsupportedMedia(f"Unsupported image type: {image.content_type}")

    body = await image.read()
    if len(body) > _MAX_IMAGE_BYTES:
        raise PayloadTooLarge("Image too large (max 10 MB)")

    return await menus.scan(
        user=user,
        image_bytes=body,
        target_language=target_language or None,
        source_language=source_language,
        restaurant_name=restaurant_name,
    )


@router.get("", response_model=list[MenuScanSummary])
async def list_scans(user: CurrentUser, menus: MenuServiceDep) -> list[MenuScanSummary]:
    return await menus.list_scans(user)


@router.get("/{scan_id}", response_model=MenuScanResponse)
async def get_scan(scan_id: UUID, user: CurrentUser, menus: MenuServiceDep) -> MenuScanResponse:
    return await menus.get_scan(user, scan_id)


@router.delete("/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scan(scan_id: UUID, user: CurrentUser, menus: MenuServiceDep) -> None:
    await menus.delete_scan(user, scan_id)


@router.post("/explain", response_model=ExplainDishResponse)
async def explain(
    payload: ExplainDishRequest, user: CurrentUser, menus: MenuServiceDep
) -> ExplainDishResponse:
    return await menus.explain_dish(
        user=user,
        dish_name=payload.dish_name,
        source_language=payload.source_language,
        target_language=payload.target_language or None,
    )
