import json
import JSONEncoderExt


class Vote:
    messageId = ""
    isUpvote = False

    def __init__(self, message_id, is_upvote):
        self.messageId = message_id
        self.isUpvote = is_upvote

    def repr_json(self):
        return dict(messageId=self.messageId, isUpvote=self.isUpvote)

votes = []


def add_vote(message_id, is_upvote):
    vote = Vote(message_id, is_upvote)
    votes.append(vote)


def clear_votes():
    del votes[:]


def get_json():
    # return json.dumps(votes, cls=JSONEncoderExt.ComplexEncoder, indent=4, separators=(',', ': '))
    return json.dumps(votes, cls=JSONEncoderExt.ComplexEncoder)
