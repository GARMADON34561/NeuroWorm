from brain.state import brain_state


def update_memory(stimulus):

    if brain_state["last_stimulus"] == stimulus:

        brain_state["stimulus_count"] += 1

    else:

        brain_state["stimulus_count"] = 1

    brain_state["last_stimulus"] = stimulus


def choose_behavior(
    left_state,
    right_state
):

    stimulus = (
        left_state,
        right_state
    )

    update_memory(
        stimulus
    )

    repetitions = (
        brain_state["stimulus_count"]
    )

    print(
        f"MEMORY={repetitions}"
    )

    # trapped

    if (
        left_state == "STRONG"
        and
        right_state == "STRONG"
    ):
        return "ESCAPE"

    # repeated trap state

    if (
        repetitions >= 3
        and
        (
            left_state == "STRONG"
            or
            right_state == "STRONG"
        )
    ):
        return "ESCAPE"

    # danger

    if (
        left_state == "STRONG"
        or
        right_state == "STRONG"
    ):
        return "AVOID"

    # curiosity

    if (
        left_state == "WEAK"
        or
        right_state == "WEAK"
    ):

        if repetitions >= 5:

            print(
                "HABITUATED"
            )

            return "EXPLORE"

        return "INVESTIGATE"

    return "EXPLORE"