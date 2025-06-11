import reflex as rx
from reflex.components.radix.themes.base import LiteralAccentColor


def flag(initials: str) -> rx.Component:
    return rx.image(
        src=f"https://flag.vercel.app/s/{initials}.svg",
        loading="lazy",
        decoding="async",
        width="24px",
        height="auto",
        border_radius="2px",
    )


def item(
    country: str, initials: str, progress: int, color: LiteralAccentColor
) -> rx.Component:
    return (
        rx.hstack(
            rx.hstack(
                flag(initials),
                rx.text(
                    country,
                    size="3",
                    weight="medium",
                    display=["none", "none", "none", "none", "flex"],
                ),
                width=["10%", "10%", "10%", "10%", "25%"],
                align="center",
                spacing="3",
            ),
            rx.flex(
                rx.text(
                    f"{progress}%",
                    position="absolute",
                    top="50%",
                    left=["90%", "90%", "90%", "90%", "95%"],
                    transform="translate(-50%, -50%)",
                    size="1",
                ),
                rx.progress(
                    value=progress,
                    height="19px",
                    color_scheme=color,
                    width="100%",
                ),
                position="relative",
                width="100%",
            ),
            width="100%",
            border_radius="10px",
            align="center",
            justify="between",
        ),
    )


def acquisition() -> rx.Component:
    return rx.vstack(
        item("Spain", "ES", 83, "amber"),
        item("USA", "US", 7, "blue"),
        item("France", "FR", 4, "plum"),
        item("Canada", "CA", 4, "crimson"),
        item("Germany", "DE", 2, "green"),
        width="100%",
        spacing="6",
    )
