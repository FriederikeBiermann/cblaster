"""A basic GUI for cblaster."""

import os
import subprocess

import PySimpleGUI as sg

from cblaster import __version__
from cblaster import main, extract as cb_extract
from cblaster.gui import search, makedb, citation, gne, extract


sg.theme("Lightgrey1")


def Column(layout, scrollable=False):
    return sg.Column(
        layout,
        scrollable=scrollable,
        size=(540, 480),
        vertical_scroll_only=True
    )


def run_cblaster(values):
    """Handles conversion of PySimpleGUI values to cblaster parameters.

    - Know which workflow tab we're on (search or makedb)
    - search
        - Know which search mode tab we're on
        - if remote, use entrez query, database, RID
        - if local, jdb and database

    Args:
        values (dict): Dictionary of values from PySimpleGUI.
    """
    if values["cblaster_tabs"] == "Search":
        args = dict(
            query_file=values["query_file"],
            query_ids=values["query_ids"],
            session_file=values["session_file"],
            mode=values["search_mode"],
            gap=values["gap"],
            unique=values["unique"],
            min_hits=values["min_hits"],
            require=values["require"],
            min_identity=values["min_identity"],
            min_coverage=values["min_coverage"],
            max_evalue=values["max_evalue"],
            recompute=values["recompute"],
        )

        if values["search_mode"] == "remote":
            args.update(
                database=values["database"],
                entrez_query=values["entrez_query"],
                rid=values["rid"]
            )
        else:
            args.update(
                database=values["dmnd_database"],
                cpus=values["cpus"]
            )

        if values["summary_gen"]:

            if values["summary_text"]:
                args["output"] = values["summary_text"]

            args.update(
                output_decimals=values["summary_decimals"],
                output_delimiter=values["summary_delimiter"],
                output_hide_headers=values["summary_hide_headers"]
            )

        if values["binary_gen"]:
            args.update(
                binary=values["binary_text"],
                binary_delimiter=values["binary_delimiter"],
                binary_hide_headers=values["binary_hide_headers"],
                binary_decimals=values["binary_decimals"],
                binary_attr=values["binary_attr"],
                binary_key=values["binary_key"],
            )

        if values["figure_gen"]:
            plot = values["figure_text"] if values["figure_text"] else True
            args.update(plot=plot)

        # Overwrite any placeholder text
        for arg, value in args.items():
            if isinstance(value, str) and value.startswith("e.g."):
                args[arg] = ""

        run_cblaster_command(values["cblaster_tabs"], args)

    elif values["cblaster_tabs"] == "Makedb":
        main.makedb(
            genbanks=values["makedb_genbanks"].split(";"),
            filename=values["makedb_filename"],
            indent=values["json_indent"]
        )

    elif values["cblaster_tabs"] == "Neighbourhood":
        main.gne(
            session=values["session"],
            output=values["output"],
            max_gap=int(values["max_gap"]),
            samples=int(values["samples"]),
            scale=values["scale"],
        )

    elif values["cblaster_tabs"] == "Extract":
        cb_extract.extract(
            values["extract_session"],
            in_cluster=values["in_cluster"],
            delimiter=values["delimiter"],
            name_only=values["name_only"],
            download=values["download"],
            output=values["extract_output"],
            queries=values["queries"],
            organisms=values["organisms"],
            scaffolds=values["scaffolds"],
        )
    else:
        raise ValueError("Expected 'Search', 'Makedb', 'Neighbourhood' or 'Extract'")


main_gui_layout = [
    [sg.Text("cblaster", font="Arial 18 bold", pad=(0, 0))],
    [sg.Text(f"v{__version__}", font="Arial 10", pad=(0, 0))],
    [sg.Text("Cameron Gilchrist, 2020", font="Arial 10", pad=(0, 0))],
    [sg.TabGroup([
        [sg.Tab("Search", [[Column(search.layout, scrollable=True)]])],
        [sg.Tab("Neighbourhood", [[Column(gne.layout)]])],
        [sg.Tab("Makedb", [[Column(makedb.layout)]])],
        [sg.Tab("Extract", [[Column(extract.layout, scrollable=True)]])],
        [sg.Tab("Citation", [[Column(citation.layout)]])],
    ], enable_events=True, key="cblaster_tabs"
    )],
    [sg.Button("Start", key="start_button", button_color=["white", "green"]),
     sg.Button("Exit", key="exit_button", button_color=["white", "red"])],
]


def cblaster_gui():

    main_window = sg.Window(
        "cblaster",
        main_gui_layout,
        size=(600, 660),
        element_padding=(5, 5),
        element_justification="center",
        finalize=True
    )
    while True:
        event, values = main_window.read()

        if event in (None, "exit_button"):
            break

        # Disable binary & summary table, figure options if not enabled
        for key in ("browse", "text", "delimiter", "decimals", "hide_headers", "key", "attr"):
            main_window[f"binary_{key}"].update(disabled=not values["binary_gen"])

        for key in ("browse", "text", "decimals", "hide_headers", "delimiter"):
            main_window[f"summary_{key}"].update(disabled=not values["summary_gen"])

        for key in ("browse", "text"):
            main_window[f"figure_{key}"].update(disabled=not values["figure_gen"])

        # Disable start button when on citation tab
        main_window["start_button"].update(
            disabled=values["cblaster_tabs"]
            not in ("Search", "Makedb", "Neighbourhood")
        )

        if event == "start_button":
            run_cblaster(values)

    main_window.close()


def run_cblaster_command(subcommand, arguments):
    command = f"cblaster {subcommand.lower()}"
    for key, value in arguments.items():
        if value in ["", False]:
            continue
        elif value is True:
            command += f" --{key}"
        else:
            command += f" --{key} {value}"
    os.system(command)


if __name__ == "__main__":
    cblaster_gui()
