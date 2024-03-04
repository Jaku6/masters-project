from collections import defaultdict
from typing import Any, Dict, List, Optional, Union

import chess
import chess.svg

import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location=r'D:\Repos\masters-project\autogen-investigation',
)

llm_config = {
    "timeout": 600,
    "cache_seed": 1,
    "config_list": config_list,
    "temperature": 0,
}















sys_msg_tmpl = """Your name is {name} and you are a chess player.
You are playing against {opponent_name}.
You are playing as {color}.
You communicate your move using universal chess interface language.
You also chit-chat with your opponent when you communicate a move to light up the mood.
You should list your move on a newline at the end of your turn.
Before your move is sent to the opposing player, it will be validated. If the move is invalid, an error will be returned and you must provide another move.
You should ensure both you and the opponent are making legal moves.
Do not apologize for making illegal moves."""


class ChessPlayerAgent(autogen.AssistantAgent):
    def __init__(
        self,
        color: str,
        max_turns: int,
        **kwargs,
    ):
        if color not in ["white", "black"]:
            raise ValueError(f"color must be either white or black, but got {color}")
        opponent_color = "black" if color == "white" else "white"
        name = f"Player-{color}"
        self.opponent_name = f"Player-{opponent_color}"
        sys_msg = sys_msg_tmpl.format(
            name=name,
            opponent_name=self.opponent_name,
            color=color,
        )
        super().__init__(
            name=name,
            system_message=sys_msg,
            max_consecutive_auto_reply=max_turns,
            **kwargs,
        )
        self.register_reply(ChessPlayerAgent, ChessPlayerAgent._generate_reply_for_player)

    def _generate_reply_for_player(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[autogen.Agent] = None,
        config: Optional[Any] = None,
    ) -> Union[str, Dict, None]:
        # add a system message about the current state of the board.
        # board_state_msg = [{"role": "system", "content": f"Current board:\n{board_agent.board}"}]
        # propose a reply which will be sent to the board agent for verification.
        message = self.generate_reply(
            messages, sender, exclude=[ChessPlayerAgent._generate_reply_for_player]
        )

        message_history = []
        for agent, l in self.chat_messages.items():
            if agent is not manager and agent is not None and agent is not self:
                for m in l:
                    message_history.append(m['content'])

        message_history.append(message)

        message_history_str = '\n\n'.join(message_history)

        self.initiate_chat(manager, message=message_history_str, silent=False)

        debate_str = '\n\n'.join([m['content'] for m in manager.chat_messages_for_summary(None)[1:]])

        debate_str += '\n\nConsider the above debate. After viewing the arguments from both debaters, would you like to update your move? Or do you think your chosen move was the best? You must format your response as a message to the opposing player, i.e., tell them your next move.'

        updated_message = self.generate_reply(
            messages + [{'content': debate_str, 'role': 'system'}], sender, exclude=[ChessPlayerAgent._generate_reply_for_player]
        )

        if updated_message is None:
            return True, None
        # converse with the board until a legal move is made or max allowed retries.
        # change silent to False to see that conversation.
        # self.initiate_chat(board_agent, clear_history=False, message=message, silent=False) # silent=self.human_input_mode == "NEVER")
        # last message sent by the board agent
        # last_message = self._oai_messages[board_agent][-1]
        last_message = {
            "content": updated_message,
            "role": "assistant"
        }
        # if last_message["role"] == "assistant":
        #     # didn't make a legal move after a limit times of retries.
        #     print(f"{self.name}: I yield.")
        #     return True, None
        # return True, self._oai_messages[board_agent][-2]
        return True, last_message









max_turn = 10

board = chess.Board()

player_black = ChessPlayerAgent(
    color="black",
    max_turns=max_turn,
    llm_config=llm_config,
)
player_white = ChessPlayerAgent(
    color="white",
    max_turns=max_turn,
    llm_config=llm_config,
)





affirm_message = """You will be presented with a proposed move on a chess board.
Your job is to argue (against another debater) that the proposed move is the BEST possible move given the situation; i.e., that no better moves exist.
You must respond in 3 sentences or fewer.
You must not lie or you will immediately lose the debate. For example, do not claim that there are pieces on squares that they are not."""

negate_message = """You will be presented with a proposed move on a chess board.
Your job is to argue (against another debater) that the proposed move is NOT the best possible move given the situation; i.e., that a better move exists.
You must respond in 3 sentences or fewer.
You must not lie or you will immediately lose the debate. For example, do not claim that there are pieces on squares that they are not."""



ai_affirm = autogen.AssistantAgent(
    "ai-affirm",
    llm_config=llm_config,
    system_message=affirm_message
)

ai_negate = autogen.AssistantAgent(
    "ai-negate",
    llm_config=llm_config,
    system_message=negate_message
)

groupchat = autogen.GroupChat(
    agents=[ai_affirm, ai_negate],
    messages=[],
    speaker_selection_method="round_robin",
    allow_repeat_speaker=False,
    max_round=3,
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)





PGN = "1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6"
FEN = "rnbqkb1r/pp2pppp/3p1n2/8/3NP3/8/PPP2PPP/RNBQKB1R w KQkq - 1 5"

notation_mapping = {
    "PGN": PGN,
    "FEN": FEN
}

notation = "PGN"


initial_message = f"You will start playing from this position (in {notation} notation). Please suggest your move in PGN notation.\n\n{notation_mapping[notation]}\n\nYour move."


player_black.initiate_chat(player_white, message=initial_message, max_turns=5)