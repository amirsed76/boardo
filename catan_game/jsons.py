# S"int" initialize
rs1 = {
    "turn": "",
    "action": {
        "title": "initialize",
        "args": ""
    },
    "players": [
        {
            "id": "for each player",
            "name": "name",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ]
}
rc1 = {
    "action": {
        "title": "done",
        "args": {
        }
    }
}
rs2 = {
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "title": "done",
        "args": {
        }
    }
}

"""
for each player 
"""
# S1
rs1 = {
    "turn": "id",
    "action": {
        "name": "place_house",
        "args": ""
    },
}
rc1 = {
    "action": {"name": "house_placed",
               "args": {
                   "tile": "int",
                   "vertex": "int"
               }
               }
}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {"name": "house_placed",
               "args": {
                   "tile": "int",
                   "vertex": "int"
               }
               }

}

# S2
rs1 = {
    "turn": "id",
    "action": {
        "name": "place_road",
        "args": ""
    },
}
rc1 = {
    "action": {
        "name": "road_placed",
        "args": {
            "tile": "int",
            "edge": {
                "v1": "int",
                "v2": "int"
            }
        }
    }
}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],

    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "road_placed",
        "args": {
            "tile": "int",
            "edge": {
                "v1": "int",
                "v2": "int"
            }
        }
    }
}

# S3  similar S1 with update parameter
rs1 = {
    "turn": "id",
    "action": {
        "name": "place_house",
        "args": ""
    }
}
rc2 = {
    "action": {
        "name": "house_placed",
        "args": {
            "tile": "int",
            "vertex": "int"
        }
    }
}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "house_placed",
        "args": {
            "tile": "int",
            "edge": {
                "v1": "int",
                "v2": "int"
            }
        }
    }
}

# S4 similar S2 with update parameter

"""
loop round 
"""
#  chance cards

# S5 noting select
rs1 = {
    "turn": "id",
    "action": {
        "name": "select_development_card",
        "args": ""
    }
}
rc1 = {
    "action": {
        "name": "selected_development_card_Null",
        "args": {
        }
    }
}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
    }
}

# S6 knight card
rs1 = {
    "turn": "id",
    "action": {
        "name": "select_development_card",
        "args": ""
    }
}
rc1 = {
    "action": {
        "name": "selected_development_card_knight",
        "args": {
            "tile": "int"
        }
    }
}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "selected_development_card_knight",
        "args": {
            "tile": "int"
        }
    }
}

# S7 select monopoly
rs1 = {
    "turn": "id",
    "action": {
        "name": "select_development_card",
        "args": ""
    }
}
rc1 = {
    "action": {
        "name": "selected_development_card_monopoly",
        "args": {
            "resource": "string"
        }
    }
}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "selected_development_card_monopoly",
        "args": {
            "resource": "string"
        }
    }
}

# S8 year of plenty
rs1 = {
    "turn": "id",
    "action": {
        "name": "select_development_card",
        "args": ""
    }
}
rc1 = {
    "action": {
        "name": "selected_development_card_year_of_plenty",
        "args": {
            "resource1": "string",
            "resource2": "string"
        }

    }
}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "selected_development_card_year_of_plenty",
        "args": {
            "resource1": "string",
            "resource2": "string"
        }
    }
}

# S9 road building
rs1 = {
    "turn": "id",
    "action": {
        "name": "select_development_card",
        "args": ""
    }
}
rc1 = {
    "action": {
        "name": "selected_development_card_year_of_road_building",
        "args": {
            "road1": {
                "edge": {
                    "v1": "int",
                    "v2": "int",
                    "resource2": "string"
                }
            },
            "road2": {
                "edge": {
                    "v1": "int",
                    "v2": "int",
                    "resource2": "string"
                }
            }
        }

    }
}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "selected_development_card_year_of_plenty",
        "args": {
            "resource1": "string",
            "resource2": "string"
        }
    }
}

# S10  dice and allocate resources
rs1 = {
    "turn": "id",
    "action": {
        "name": "dice",
        "args": {
        }
    }
}
rc1 = {
    "action": {
        "name": "rolled_dice",
        "args": ""
    }

}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "rolled_dice",
        "args": {
            "number1": "int",
            "number2": "int"

        }
    }

}

# S11 buy and build house
rs1 = {
    "turn": "id",
    "action": {
        "name": "trade_buy_build",
        "args": {
        }
    }
}
rc1 = {
    "action": {
        "name": "build_house",
        "args": {
            "tile": "int",
            "vertex": "int"
        }
    }
}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "build_house",
        "args": {
            "tile": "int",
            "vertex": "int"
        }
    }
}

# S12  buy and build road
rs1 = {
    "turn": "id",
    "action": {
        "name": "trade_buy_build",
        "args": {
        }
    }
}
rc1 = {
    "action": {
        "name": "build_road",
        "args": {
            "tile": "int",
            "edge": {
                "v1": "int",
                "v2": "int"
            }
        }
    }

}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "build_road",
        "args": {
            "tile": "int",
            "edge": {
                "v1": "int",
                "v2": "int"
            }
        }
    }
}

# S13 buy and city
rs1 = {
    "turn": "id",
    "action": {
        "name": "trade_buy_build",
        "args": {
        }
    }
}
rc1 = {
    "action": {
        "name": "build_house",
        "args": {
            "tile": "int",
            "vertex": "int"
        }
    }

}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "build_house",
        "args": {
            "tile": "int",
            "vertex": "int"
        }
    }
}

# S14 buy development card
rs1 = {
    "turn": "id",
    "action": {
        "name": "trade_buy_build",
        "args": {
        }
    }
}
rc1 = {
    "action": {
        "name": "get_development_card",
        "args": {
        }
    }
}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "get_development_card",
        "args": ""
    }
}

# S15 trade request
rs1 = {
    "turn": "id",
    "action": {
        "name": "trade_buy_build",
        "args": {
        }
    }
}
rc1 = {
    "action": {
        "name": "trade_request",
        "args": {
            "want": {"brick": "int",
                     "sheep": "int",
                     "stone": "int",
                     "wheat": "int",
                     "wood": "int"
                     },
            "give": {"brick": "int",
                     "sheep": "int",
                     "stone": "int",
                     "wheat": "int",
                     "wood": "int"
                     }

        }
    }
}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "trade_request",
        "args": {
            "want": {"brick": "int",
                     "sheep": "int",
                     "stone": "int",
                     "wheat": "int",
                     "wood": "int"
                     },
            "give": {"brick": "int",
                     "sheep": "int",
                     "stone": "int",
                     "wheat": "int",
                     "wood": "int"
                     }

        }
    }

}

# S16 accept trade
rs1 = {
    "turn": "all",
    "action": {
        "name": "accept_reject_trade",
        "args": {
        }
    }
}
rc1 = {
    "action": {
        "name": "trade_accepted",
        "args": {
        }
    }
}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "trade_response",
        "args": {
            "player1": {
                "state": "bool",
                "description": "text"
            },
            "player2": {
                "state": "bool",
                "description": "text"

            },
            "player3": {
                "state": "bool",
                "description": "text"

            }
            , "player4": {
                "state": "bool",
                "description": "text"

            }
        }
    }

}

# S17 reject trade
rs1 = {
    "turn": "all",
    "action": {
        "name": "accept_reject_trade",
        "args": {
        }
    }
}
rc1 = {
    "action": {
        "name": "trade_rejected",
        "args": {
            "description": "text"
        }
    }
}
rs2 = {
    "turn": "id",
    "personal": {
        "resource": {
            "brick": "int",
            "sheep": "int",
            "stone": "int",
            "wheat": "int",
            "wood": "int"
        },
        "cards": {
            "knight": "int",
            "monopoly": "int",
            "road_building": "int",
            "year_of_plenty": "int",
            "victory": "int"
        }
    },
    "players": [
        {
            "id": "for each player",
            "cards": "int",
            "resources": "int",
            "point": "int",
            "road_length": "int"
        }
    ],
    "longest_road": "player_id",
    "largest_army": "player_id",
    "update": {
        "name": "trade_response",
        "args": {
            "player1": {
                "state": "bool",
                "description": "text"
            },
            "player2": {
                "state": "bool",
                "description": "text"

            },
            "player3": {
                "state": "bool",
                "description": "text"

            }
            , "player4": {
                "state": "bool",
                "description": "text"

            }
        }
    }

}

# S18 finish game
rs1 = {
    "turn": "all",
    "action": {
        "name": "finish",
        "args": {
            "players": {
                "player1": "int",
                "player2": "int",
                "player3": "int",
                "player4": "int"

            },
            "winner": "player_id"
        }
    }
}
rc1 = {
    "action": {
        "name": "star_comment",
        "args": {
            "star": "int",
            "comment": "text"
        }
    }
}

rs2 = None  # disconnect user
