# ============================================================
# PRIVI-BROWSER
# Task Planner
# ============================================================


import re


class TaskPlanner:

    def plan(self, task):

        task = task.strip()

        actions = []

        # Split combined tasks
        parts = (
            task
            .replace(" and then ", "|")
            .replace(" then ", "|")
            .replace(" after that ", "|")
        ).split("|")

        for part in parts:

            part = part.strip()

            if not part:
                continue

            action = self.detect_action(part)

            if action:
                actions.append(action)

        return actions


    # --------------------------------------------------------
    # Detect individual action
    # --------------------------------------------------------

    def detect_action(self, task):

        lower = task.lower().strip()


        # ----------------------------------------------------
        # YOUTUBE SEARCH
        # ----------------------------------------------------

        if lower.startswith("search youtube"):

            query = task[len("search youtube"):].strip()

            query = re.sub(
                r"^(for|about)\s+",
                "",
                query,
                flags=re.IGNORECASE
            ).strip()

            return {
                "action": "search_youtube",
                "target": query
            }


        # ----------------------------------------------------
        # GOOGLE SEARCH
        # ----------------------------------------------------

        if lower.startswith("search google"):

            query = task[len("search google"):].strip()

            query = re.sub(
                r"^(for|about)\s+",
                "",
                query,
                flags=re.IGNORECASE
            ).strip()

            return {
                "action": "search_google",
                "target": query
            }


        # ----------------------------------------------------
        # YOUTUBE / GOOGLE OPEN
        # ----------------------------------------------------

        if lower.startswith("open youtube"):

            return {
                "action": "open",
                "target": "youtube"
            }


        if lower.startswith("open google"):

            return {
                "action": "open",
                "target": "google"
            }


        # ----------------------------------------------------
        # PLAY
        # ----------------------------------------------------

        if (
            lower == "play" or
            lower == "play video" or
            lower == "start video" or
            lower == "resume video"
        ):

            return {
                "action": "play",
                "target": "video"
            }


        if lower.startswith("play "):

            target = task[len("play"):].strip()

            if target:

                return {
                    "action": "play",
                    "target": target
                }


        # ----------------------------------------------------
        # PAUSE
        # ----------------------------------------------------

        if (
            lower == "pause" or
            lower == "pause video" or
            lower == "pause the video"
        ):

            return {
                "action": "pause",
                "target": "video"
            }


        # ----------------------------------------------------
        # STOP
        # ----------------------------------------------------

        if (
            lower == "stop" or
            lower == "stop video" or
            lower == "stop the video"
        ):

            return {
                "action": "stop",
                "target": "video"
            }


        # ----------------------------------------------------
        # LIKE
        # IMPORTANT: CHECK UNLIKE FIRST
        # ----------------------------------------------------

        if (
            lower == "unlike" or
            "unlike the video" in lower or
            "remove like" in lower or
            "remove the like" in lower
        ):

            return {
                "action": "unlike",
                "target": "video"
            }


        if (
            lower == "like" or
            lower == "like video" or
            lower == "like the video" or
            "like this video" in lower
        ):

            return {
                "action": "like",
                "target": "video"
            }


        # ----------------------------------------------------
        # DISLIKE
        # ----------------------------------------------------

        if (
            lower == "dislike" or
            lower == "dislike video" or
            lower == "dislike the video" or
            "dislike this video" in lower
        ):

            return {
                "action": "dislike",
                "target": "video"
            }


        # ----------------------------------------------------
        # SUBSCRIBE
        # ----------------------------------------------------

        if (
            lower == "unsubscribe" or
            "unsubscribe from the channel" in lower or
            "unsubscribe channel" in lower
        ):

            return {
                "action": "unsubscribe",
                "target": "channel"
            }


        if (
            lower == "subscribe" or
            lower == "subscribe channel" or
            "subscribe to the channel" in lower or
            "subscribe the channel" in lower
        ):

            return {
                "action": "subscribe",
                "target": "channel"
            }


        # ----------------------------------------------------
        # FOLLOW
        # ----------------------------------------------------

        if (
            lower == "unfollow" or
            "unfollow this account" in lower or
            "unfollow the account" in lower or
            "unfollow this page" in lower
        ):

            return {
                "action": "unfollow",
                "target": "account"
            }


        if (
            lower == "follow" or
            "follow this account" in lower or
            "follow the account" in lower or
            "follow this page" in lower
        ):

            return {
                "action": "follow",
                "target": "account"
            }


        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        if (
            lower == "unsave" or
            "remove from saved" in lower or
            "remove from saved items" in lower
        ):

            return {
                "action": "unsave",
                "target": "post"
            }


        if (
            lower == "save" or
            lower == "save post" or
            lower == "save this post" or
            lower == "save video" or
            lower == "save this video" or
            lower == "save reel" or
            lower == "save this reel"
        ):

            return {
                "action": "save",
                "target": "content"
            }


        # ----------------------------------------------------
        # SHARE
        # ----------------------------------------------------

        if (
            lower == "share" or
            lower == "share video" or
            lower == "share this video" or
            lower == "share post" or
            lower == "share this post"
        ):

            return {
                "action": "share",
                "target": "content"
            }


        # ----------------------------------------------------
        # COMMENT
        # ----------------------------------------------------

        if lower.startswith("comment "):

            comment = task[len("comment "):].strip()

            return {
                "action": "comment",
                "target": comment
            }


        # ----------------------------------------------------
        # SEND
        # ----------------------------------------------------

        if lower.startswith("send "):

            message = task[len("send "):].strip()

            return {
                "action": "send",
                "target": message
            }


        # ----------------------------------------------------
        # VOLUME UP
        # ----------------------------------------------------

        if (
            lower == "volume up" or
            lower == "increase volume" or
            lower == "increase sound" or
            lower == "raise volume" or
            lower == "make it louder" or
            lower == "sound up" or
            lower == "louder" or
            lower == "more volume"
        ):

            return {
                "action": "volume_up",
                "target": "video"
            }


        # ----------------------------------------------------
        # VOLUME DOWN
        # ----------------------------------------------------

        if (
            lower == "volume down" or
            lower == "decrease volume" or
            lower == "decrease sound" or
            lower == "lower volume" or
            lower == "make it quieter" or
            lower == "sound down" or
            lower == "quieter" or
            lower == "less volume"
        ):

            return {
                "action": "volume_down",
                "target": "video"
            }


        # ----------------------------------------------------
        # MUTE
        # ----------------------------------------------------

        if (
            lower == "mute" or
            lower == "mute video" or
            lower == "mute the video"
        ):

            return {
                "action": "mute",
                "target": "video"
            }


        # ----------------------------------------------------
        # UNMUTE
        # ----------------------------------------------------

        if (
            lower == "unmute" or
            lower == "unmute video" or
            lower == "unmute the video"
        ):

            return {
                "action": "unmute",
                "target": "video"
            }


        # ----------------------------------------------------
        # NEXT VIDEO
        # ----------------------------------------------------

        if (
            lower == "next" or
            lower == "next video" or
            lower == "play next video" or
            lower == "go to next video"
        ):

            return {
                "action": "next",
                "target": "video"
            }


        # ----------------------------------------------------
        # PREVIOUS VIDEO
        # ----------------------------------------------------

        if (
            lower == "previous" or
            lower == "previous video" or
            lower == "prev video" or
            lower == "go to previous video"
        ):

            return {
                "action": "previous",
                "target": "video"
            }


        # ----------------------------------------------------
        # SKIP FORWARD
        # ----------------------------------------------------

        if (
            lower == "skip" or
            lower == "skip video" or
            lower == "skip forward" or
            lower == "skip ahead"
        ):

            return {
                "action": "seek_forward",
                "target": "10"
            }


        # ----------------------------------------------------
        # SKIP BACKWARD
        # ----------------------------------------------------

        if (
            lower == "go back" or
            lower == "go backward" or
            lower == "skip backward"
        ):

            return {
                "action": "seek_backward",
                "target": "10"
            }


        # ----------------------------------------------------
        # SEEK FORWARD X SECONDS
        # ----------------------------------------------------

        match = re.search(
            r"(?:forward|ahead|skip)\s+(\d+)\s*(?:seconds?|secs?)?",
            lower
        )

        if match:

            seconds = match.group(1)

            return {
                "action": "seek_forward",
                "target": seconds
            }


        # ----------------------------------------------------
        # SEEK BACKWARD X SECONDS
        # ----------------------------------------------------

        match = re.search(
            r"(?:backward|back|rewind)\s+(\d+)\s*(?:seconds?|secs?)?",
            lower
        )

        if match:

            seconds = match.group(1)

            return {
                "action": "seek_backward",
                "target": seconds
            }


        # ----------------------------------------------------
        # FULLSCREEN
        # ----------------------------------------------------

        if (
            lower == "fullscreen" or
            lower == "full screen" or
            lower == "make fullscreen" or
            lower == "enter fullscreen"
        ):

            return {
                "action": "fullscreen",
                "target": "video"
            }


        # ----------------------------------------------------
        # WAIT
        # ----------------------------------------------------

        match = re.search(
            r"(?:wait|sleep)\s+(\d+)\s*(?:seconds?|secs?)?",
            lower
        )

        if match:

            seconds = match.group(1)

            return {
                "action": "wait",
                "target": seconds
            }


        # ----------------------------------------------------
        # SCROLL DOWN
        # ----------------------------------------------------

        if (
            "scroll down" in lower or
            "scroll more" in lower or
            "show more" in lower or
            "more videos" in lower
        ):

            return {
                "action": "scroll",
                "target": "down"
            }


        # ----------------------------------------------------
        # SCROLL UP
        # ----------------------------------------------------

        if (
            "scroll up" in lower or
            "go up" in lower
        ):

            return {
                "action": "scroll",
                "target": "up"
            }


        # ----------------------------------------------------
        # OPEN WEBSITE
        # ----------------------------------------------------

        websites = [
            "youtube",
            "google",
            "instagram",
            "facebook",
            "amazon",
            "flipkart",
            "github",
            "linkedin",
            "gmail",
            "spotify",
            "netflix",
            "chatgpt"
        ]


        for site in websites:

            if (
                lower == f"open {site}" or
                lower == f"go to {site}"
            ):

                return {
                    "action": "open",
                    "target": site
                }


        # ----------------------------------------------------
        # CLICK
        # ----------------------------------------------------

        if (
            lower.startswith("click ") or
            lower.startswith("press ") or
            lower.startswith("tap ")
        ):

            target = task.split(
                " ",
                1
            )[1].strip()

            return {
                "action": "click",
                "target": target
            }


        # ----------------------------------------------------
        # TYPE
        # ----------------------------------------------------

        if lower.startswith("type "):

            text = task[
                len("type "):
            ].strip()

            return {
                "action": "type",
                "target": text
            }


        # ----------------------------------------------------
        # UNKNOWN
        # ----------------------------------------------------

        return {
            "action": "unknown",
            "target": task
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    planner = TaskPlanner()


    test_tasks = [

        "Search YouTube for ISRO videos and then play",

        "increase volume",

        "decrease volume",

        "follow",

        "unfollow",

        "like",

        "unlike",

        "dislike",

        "subscribe",

        "unsubscribe",

        "save",

        "unsave",

        "share",

        "skip video",

        "wait 5 seconds",

        "scroll down",

        "scroll up",

        "mute",

        "unmute",

        "next video",

        "previous video",

        "fullscreen"

    ]


    print("\n🧠 PRIVI-BROWSER TASK PLANNER")
    print("--------------------------------")


    for test_task in test_tasks:

        result = planner.plan(
            test_task
        )

        print(
            f"\nUser Task: {test_task}"
        )

        print("Generated Plan:")

        for index, action in enumerate(
            result,
            start=1
        ):

            print(
                f"{index}. "
                f"{action['action']} "
                f"→ "
                f"{action['target']}"
            )