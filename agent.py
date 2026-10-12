# ============================================================
# PRIVI-BROWSER
# AI Browser Agent - Agent Core
# ============================================================


from planner import TaskPlanner
class BrowserAgent:

    def __init__(self):
        self.current_task = None
        self.steps = []
        self.planner = TaskPlanner()


    # --------------------------------------------------------
    # Understand user task
    # --------------------------------------------------------

    def understand_task(self, task):

        task = str(task).strip()

        self.current_task = task

        return {
            "task": task,
            "understood": bool(task)
        }


    # --------------------------------------------------------
    # Extract text after a phrase
    # --------------------------------------------------------

    def extract_after(self, text, phrase):

        if phrase in text:
            return text.split(phrase, 1)[1].strip()

        return ""


    # --------------------------------------------------------
    # Create action plan
    # --------------------------------------------------------

    def create_plan(self, task):

        task_lower = task.lower().strip()

        steps = []


        if not task_lower:
            self.steps = []

            return steps


        # ====================================================
        # OPEN WEBSITE
        # ====================================================

        if "open youtube" in task_lower:

            steps.append({
                "action": "open",
                "target": "youtube"
            })


        elif "open google" in task_lower:

            steps.append({
                "action": "open",
                "target": "google"
            })


        elif "open instagram" in task_lower:

            steps.append({
                "action": "open",
                "target": "instagram"
            })


        elif "open facebook" in task_lower:

            steps.append({
                "action": "open",
                "target": "facebook"
            })


        elif "open linkedin" in task_lower:

            steps.append({
                "action": "open",
                "target": "linkedin"
            })


        # ====================================================
        # YOUTUBE SEARCH
        # ====================================================

        if "search youtube" in task_lower:

            query = self.extract_after(
                task_lower,
                "search youtube"
            )

            query = query.removeprefix("for ").strip()

            if query:

                steps.append({
                    "action": "search_youtube",
                    "target": query
                })


        elif "youtube search" in task_lower:

            query = self.extract_after(
                task_lower,
                "youtube search"
            )

            query = query.removeprefix("for ").strip()

            if query:

                steps.append({
                    "action": "search_youtube",
                    "target": query
                })


        # ====================================================
        # GOOGLE SEARCH
        # ====================================================

        if "search google" in task_lower:

            query = self.extract_after(
                task_lower,
                "search google"
            )

            query = query.removeprefix("for ").strip()

            if query:

                steps.append({
                    "action": "search_google",
                    "target": query
                })


        elif "search for" in task_lower:

            query = self.extract_after(
                task_lower,
                "search for"
            ).strip()

            if query:

                steps.append({
                    "action": "search_google",
                    "target": query
                })


        # ====================================================
        # PLAY
        # ====================================================

        if (
            task_lower == "play" or
            task_lower == "play video" or
            task_lower == "resume" or
            task_lower == "resume video" or
            "play the video" in task_lower or
            "play this video" in task_lower or
            "resume the video" in task_lower or
            "continue playing" in task_lower
        ):

            steps.append({
                "action": "play",
                "target": "video"
            })


        # ====================================================
        # PAUSE
        # ====================================================

        if (
            task_lower == "pause" or
            task_lower == "pause video" or
            "pause the video" in task_lower or
            "pause this video" in task_lower
        ):

            steps.append({
                "action": "pause",
                "target": "video"
            })


        # ====================================================
        # STOP
        # ====================================================

        if (
            task_lower == "stop" or
            task_lower == "stop video" or
            "stop the video" in task_lower
        ):

            steps.append({
                "action": "stop",
                "target": "video"
            })


        # ====================================================
        # LIKE
        # ====================================================

        if (
            task_lower == "like" or
            "like this" in task_lower or
            "like the video" in task_lower or
            "like the post" in task_lower or
            "give it a like" in task_lower or
            "click like" in task_lower
        ):

            steps.append({
                "action": "like",
                "target": "video"
            })


        # ====================================================
        # UNLIKE
        # ====================================================

        if (
            task_lower == "unlike" or
            "unlike this" in task_lower or
            "unlike the video" in task_lower or
            "unlike the post" in task_lower or
            "remove like" in task_lower
        ):

            steps.append({
                "action": "unlike",
                "target": "video"
            })


        # ====================================================
        # DISLIKE
        # ====================================================

        if (
            task_lower == "dislike" or
            "dislike this" in task_lower or
            "dislike the video" in task_lower or
            "give it a dislike" in task_lower or
            "click dislike" in task_lower
        ):

            steps.append({
                "action": "dislike",
                "target": "video"
            })


        # ====================================================
        # SUBSCRIBE
        # ====================================================

        if (
            task_lower == "subscribe" or
            "subscribe to" in task_lower or
            "subscribe channel" in task_lower or
            "click subscribe" in task_lower
        ):

            steps.append({
                "action": "subscribe",
                "target": "channel"
            })


        # ====================================================
        # UNSUBSCRIBE
        # ====================================================

        if (
            task_lower == "unsubscribe" or
            "un subscribe" in task_lower or
            "cancel subscription" in task_lower
        ):

            steps.append({
                "action": "unsubscribe",
                "target": "channel"
            })


        # ====================================================
        # FOLLOW
        # ====================================================

        if (
            task_lower == "follow" or
            "follow this" in task_lower or
            "follow this person" in task_lower or
            "follow account" in task_lower or
            "click follow" in task_lower
        ):

            steps.append({
                "action": "follow",
                "target": "account"
            })


        # ====================================================
        # UNFOLLOW
        # ====================================================

        if (
            task_lower == "unfollow" or
            "unfollow this" in task_lower or
            "unfollow account" in task_lower or
            "stop following" in task_lower or
            "remove follow" in task_lower
        ):

            steps.append({
                "action": "unfollow",
                "target": "account"
            })


        # ====================================================
        # SAVE
        # ====================================================

        if (
            task_lower == "save" or
            "save this" in task_lower or
            "save the post" in task_lower or
            "save the video" in task_lower or
            "bookmark this" in task_lower or
            "bookmark it" in task_lower
        ):

            steps.append({
                "action": "save",
                "target": "content"
            })


        # ====================================================
        # SHARE
        # ====================================================

        if (
            task_lower == "share" or
            "share this" in task_lower or
            "share the post" in task_lower or
            "share the video" in task_lower or
            "click share" in task_lower
        ):

            steps.append({
                "action": "share",
                "target": "content"
            })


        # ====================================================
        # COMMENT
        # ====================================================

        if (
            task_lower == "comment" or
            "open comments" in task_lower or
            "show comments" in task_lower or
            "click comment" in task_lower
        ):

            steps.append({
                "action": "comment",
                "target": "content"
            })


        # ====================================================
        # SEND
        # ====================================================

        if (
            task_lower == "send" or
            "click send" in task_lower or
            "press send" in task_lower
        ):

            steps.append({
                "action": "send",
                "target": "message"
            })


        # ====================================================
        # VOLUME UP
        # ====================================================

        if (
            task_lower == "volume up" or
            "increase volume" in task_lower or
            "increase sound" in task_lower or
            "raise volume" in task_lower or
            "make it louder" in task_lower or
            "sound up" in task_lower or
            "make it loud" in task_lower
        ):

            steps.append({
                "action": "volume_up",
                "target": "video"
            })


        # ====================================================
        # VOLUME DOWN
        # ====================================================

        if (
            task_lower == "volume down" or
            "decrease volume" in task_lower or
            "decrease sound" in task_lower or
            "lower volume" in task_lower or
            "make it quieter" in task_lower or
            "sound down" in task_lower or
            "make it quiet" in task_lower
        ):

            steps.append({
                "action": "volume_down",
                "target": "video"
            })


        # ====================================================
        # MUTE
        # ====================================================

        if (
            task_lower == "mute" or
            "mute video" in task_lower or
            "mute the video" in task_lower or
            "turn off sound" in task_lower or
            "make it silent" in task_lower
        ):

            steps.append({
                "action": "mute",
                "target": "video"
            })


        # ====================================================
        # UNMUTE
        # ====================================================

        if (
            task_lower == "unmute" or
            "unmute video" in task_lower or
            "turn on sound" in task_lower or
            "enable sound" in task_lower
        ):

            steps.append({
                "action": "unmute",
                "target": "video"
            })


        # ====================================================
        # SCROLL DOWN
        # ====================================================

        if (
            "scroll down" in task_lower or
            "scroll more" in task_lower or
            "show more" in task_lower or
            "go down" in task_lower or
            "move down" in task_lower
        ):

            steps.append({
                "action": "scroll",
                "target": "down"
            })


        # ====================================================
        # SCROLL UP
        # ====================================================

        if (
            "scroll up" in task_lower or
            "go up" in task_lower or
            "move up" in task_lower or
            "scroll higher" in task_lower
        ):

            steps.append({
                "action": "scroll",
                "target": "up"
            })


        # ====================================================
        # NEXT VIDEO
        # ====================================================

        if (
            task_lower == "next" or
            "next video" in task_lower or
            "play next video" in task_lower or
            "go to next video" in task_lower
        ):

            steps.append({
                "action": "next",
                "target": "video"
            })


        # ====================================================
        # PREVIOUS VIDEO
        # ====================================================

        if (
            task_lower == "previous" or
            "previous video" in task_lower or
            "go to previous video" in task_lower
        ):

            steps.append({
                "action": "previous",
                "target": "video"
            })


        # ====================================================
        # SEEK / SKIP FORWARD
        # ====================================================

        if (
            "seek forward" in task_lower or
            "fast forward" in task_lower or
            "skip forward" in task_lower or
            "skip video" in task_lower or
            "move forward in the video" in task_lower
        ):

            steps.append({
                "action": "seek_forward",
                "target": "video"
            })


        # ====================================================
        # SEEK / SKIP BACKWARD
        # ====================================================

        if (
            "seek backward" in task_lower or
            "rewind" in task_lower or
            "skip backward" in task_lower or
            "move backward in the video" in task_lower
        ):

            steps.append({
                "action": "seek_backward",
                "target": "video"
            })


        # ====================================================
        # FULLSCREEN
        # ====================================================

        if (
            "fullscreen" in task_lower or
            "full screen" in task_lower or
            "expand video" in task_lower
        ):

            steps.append({
                "action": "fullscreen",
                "target": "video"
            })


        # ====================================================
        # WAIT
        # ====================================================

        wait_words = (
            "wait",
            "pause for",
            "sleep for"
        )

        for word in wait_words:

            if task_lower.startswith(word):

                remaining = task_lower[
                    len(word):
                ].strip()

                number = ""

                for char in remaining:

                    if char.isdigit() or char == ".":

                        number += char

                    elif number:

                        break

                if number:

                    try:

                        seconds = float(number)

                        if 0 < seconds <= 300:

                            steps.append({
                                "action": "wait",
                                "target": seconds
                            })

                    except ValueError:
                        pass

                break


        # ====================================================
        # PLAY / WATCH SEARCH
        # ====================================================

        if (
            task_lower.startswith("play ") and
            task_lower not in (
                "play video",
                "play the video",
                "play this video"
            )
        ):

            query = task_lower[5:].strip()

            if query:

                steps.append({
                    "action": "play_search",
                    "target": query
                })


        elif task_lower.startswith("watch "):

            query = task_lower[6:].strip()

            if query:

                steps.append({
                    "action": "play_search",
                    "target": query
                })


        # Save plan

        self.steps = steps

        return steps


        # --------------------------------------------------------
    # Full agent process
    # --------------------------------------------------------

    def process_task(self, task):

        understanding = self.understand_task(task)

        plan = self.planner.plan(task)

        self.steps = plan

        return {
            "understanding": understanding,
            "plan": plan
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    agent = BrowserAgent()


    test_tasks = [
        "Search YouTube for ISRO videos and play",
        "increase volume",
        "decrease volume",
        "follow",
        "unfollow",
        "wait 5 seconds",
        "skip video",
        "like",
        "unlike",
        "dislike",
        "subscribe"
    ]


    print("\n🤖 PRIVI-BROWSER AGENT")
    print("----------------------")


    for task in test_tasks:

        result = agent.process_task(task)

        print("\nTask:")
        print(task)

        print("Plan:")

        for step in result["plan"]:

            print(
                f"- {step['action']} → {step['target']}"
            )