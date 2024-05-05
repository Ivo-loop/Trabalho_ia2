
#pontuação por peça para calculo de melhor jogada
#obs: dependo do valor da peça temos jogadas diferentes e recriamos novas estrategias.
BOARD_SCORES = {
    "PAWN": 1,
    "BISHOP": 4,
    "KING": 50,
    "QUEEN": 10,
    "KNIGHT": 5,
    "ROOK": 3
}

# max board score for player == 42 < WIN
END_SCORES = {
    "WIN": 100,
    "LOSE": -100,
    "TIE": 0,
}


PIECES = {
    1: "PAWN",
    2: "KNIGHT",
    3: "BISHOP",
    4: "ROOK",
    5: "QUEEN",
    6: "KING"
}