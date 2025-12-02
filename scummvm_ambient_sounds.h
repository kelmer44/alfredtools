// Alfred Pelrock - Room Ambient Sound Configuration
// Auto-generated for ScummVM implementation
//
// TIMING CONSTANTS:
// #define AMBIENT_TIMER_HZ       70
// #define AMBIENT_TIMER_TICKS    1090
// #define AMBIENT_INTERVAL_MS    15571
//
// BEHAVIOR:
// - Increment timer each game tick (70Hz / ~14ms)
// - Reset timer to 0 on any mouse movement
// - When timer > 1090, pick random sound from room's active slots
// - Play sound at volume 256 (center stereo)
// - Reset timer after playing

struct RoomAmbientSound {
    uint8 musicTrack;
    uint8 soundSlots[9];  // Index into SOUND_FILENAMES, 0 = none
};

static const RoomAmbientSound ROOM_SOUNDS[] = {
    /* Room  0 */ {  0, { 41, 42,  4,  0,  7,  2,  3, 10,  0 } },
    /* Room  1 */ {  1, {  0,  0,  0,  0,  7,  8,  9, 13,  0 } },
    /* Room  2 */ {  1, { 41, 42,  0,  0,  6,  7, 10,  1, 45 } },
    /* Room  3 */ {  1, { 41, 42, 40,  0, 10, 13,  8, 20,  0 } },
    /* Room  4 */ {  1, { 41, 42, 38,  0,  1, 18, 21, 22,  0 } },
    /* Room  5 */ {  2, { 28,  0,  0,  0, 23,  0,  0,  0,  0 } },
    /* Room  6 */ {  2, {  0,  0,  0,  0, 28, 23,  0,  0,  0 } },
    /* Room  7 */ {  6, { 43,  0,  0,  0,  0,  0,  0,  0,  0 } },
    /* Room  8 */ {  1, { 41, 42,  0,  0, 19,  8,  3, 21,  0 } },
    /* Room  9 */ {  2, { 41, 42, 26,  0,  0,  0,  0,  0, 25 } },
    /* Room 10 */ {  1, { 41, 42,  0,  0,  6,  7, 10,  1, 45 } },
    /* Room 11 */ {  1, { 41, 42,  0,  0,  6,  7, 10,  1, 45 } },
    /* Room 12 */ {  4, { 41, 42,  0,  0, 29,  0,  0,  0,  0 } },
    /* Room 13 */ {  5, { 41, 42, 44,  0, 31,  0,  0,  0, 30 } },
    /* Room 14 */ {  1, {  0,  0,  0,  0,  3,  8,  9, 10,  0 } },
    /* Room 15 */ {  0, {  0,  0,  0,  0,  0,  0,  0,  0,  0 } },
    /* Room 16 */ {  1, { 41, 42,  0,  0, 33,  2,  9, 14,  0 } },
    /* Room 17 */ {  0, { 41, 42,  0,  0, 68, 35, 27, 59, 25 } },
    /* Room 18 */ {  0, {  0,  0,  0,  0,  1, 21,  6,  0,  0 } },
    /* Room 19 */ {  1, { 65, 66, 24,  0,  8, 18,  4, 10, 38 } },
    /* Room 20 */ {  3, { 96,  0,  0,  0, 27,  0,  0,  0,  0 } },
    /* Room 21 */ {  7, {  0,  0,  0,  0, 70, 92, 93, 94,  0 } },
    /* Room 22 */ {  8, {  0,  0,  0,  0, 26, 70, 61,  0,  0 } },
    /* Room 23 */ {  8, {  0,  0,  0,  0, 70,  0,  0,  0,  0 } },
    /* Room 24 */ {  8, { 77,  0,  0,  0, 70, 48, 49,  0,  0 } },
    /* Room 25 */ {  8, { 47,  0,  0,  0, 70, 48, 79,  0,  0 } },
    /* Room 26 */ {  9, {  0,  0,  0,  0, 60, 61, 53, 70,  0 } },
    /* Room 27 */ {  9, {  0,  0,  0,  0, 60, 61, 53, 70,  0 } },
    /* Room 28 */ { 13, { 91,  0,  0,  0, 62,  0, 47,  0,  0 } },
    /* Room 29 */ {  8, { 41, 42,  0,  0, 70,  0,  0,  0,  0 } },
    /* Room 30 */ {  0, { 74,  0,  0,  0, 55, 56,  0,  0,  0 } },
    /* Room 31 */ { 10, {  0,  0,  0,  0, 80, 57, 30,  0,  0 } },
    /* Room 32 */ { 11, {  0,  0,  0,  0,  0,  0,  0,  0,  0 } },
    /* Room 33 */ { 11, { 41, 42,  0,  0,  0,  0,  0,  0, 57 } },
    /* Room 34 */ {  8, {  0,  0,  0,  0, 70,  0,  0,  0, 54 } },
    /* Room 35 */ { 12, {  0,  0,  0,  0, 75, 70,  0,  0, 73 } },
    /* Room 36 */ {  8, { 83,  0,  0,  0, 70,  0,  0,  0,  0 } },
    /* Room 37 */ {  0, {  0,  0,  0,  0, 70,  0,  0,  0, 82 } },
    /* Room 38 */ { 11, {  0,  0,  0,  0,  0,  0,  0,  0,  0 } },
    /* Room 39 */ { 14, { 81,  0,  0,  0, 79,  0,  0,  0,  0 } },
    /* Room 40 */ { 15, {  0,  0,  0,  0,  0,  0,  0,  0,  0 } },
    /* Room 41 */ { 16, { 46, 69, 74,  0, 63, 65, 70, 64,  0 } },
    /* Room 42 */ { 16, {  0,  0,  0,  0, 63, 64, 65, 70,  0 } },
    /* Room 43 */ { 17, {  0,  0,  0,  0, 70,  0,  0,  0,  0 } },
    /* Room 44 */ { 17, { 83,  0,  0,  0, 70,  0,  0,  0,  0 } },
    /* Room 45 */ { 18, { 95,  0,  0,  0, 70, 79,  0,  0,  0 } },
    /* Room 46 */ { 19, { 41, 42, 87,  0, 78, 43, 10,  0, 57 } },
    /* Room 47 */ {  0, {  0,  0,  0,  0, 52, 10,  0,  0,  0 } },
    /* Room 48 */ { 23, { 74,  0,  0,  0,  0,  0,  0,  0,  0 } },
    /* Room 49 */ { 20, {  0,  0,  0,  0, 78, 43,  0,  0, 84 } },
    /* Room 50 */ { 20, {  0,  0,  0,  0, 78, 43,  0,  0, 84 } },
    /* Room 51 */ { 22, { 85, 86, 87,  0, 78, 43, 88, 89, 84 } },
    /* Room 52 */ { 22, { 85, 86, 87, 45, 78, 43, 89, 90, 84 } },
    /* Room 53 */ { 22, { 85, 86, 87,  0, 78, 43, 88, 90, 84 } },
    /* Room 54 */ { 22, { 85, 86, 87,  0, 78, 43, 88, 90, 84 } },
    /* Room 55 */ { 21, {  0,  0,  0,  0,  0,  0,  0,  0,  0 } },
};

// Sound filename lookup table
static const char* SOUND_FILENAMES[] = {
    /*  0 */ "NO_SOUND.wav",
    /*  1 */ "BUHO_ZZZ.wav",
    /*  2 */ "BIRD_1_1.wav",
    /*  3 */ "BIRD_1_2.wav",
    /*  4 */ "BIRD_1_3.wav",
    /*  5 */ "DESPERZZ.wav",
    /*  6 */ "HORN_5ZZ.wav",
    /*  7 */ "HORN_6ZZ.wav",
    /*  8 */ "HORN_8ZZ.wav",
    /*  9 */ "SUZIPASS.wav",
    /* 10 */ "CAT_1ZZZ.wav",
    /* 11 */ "DOG_01ZZ.wav",
    /* 12 */ "DOG_02ZZ.wav",
    /* 13 */ "DOG_04ZZ.wav",
    /* 14 */ "DOG_05ZZ.wav",
    /* 15 */ "DOG_06ZZ.wav",
    /* 16 */ "DOG_07ZZ.wav",
    /* 17 */ "DOG_09ZZ.wav",
    /* 18 */ "ALARMZZZ.wav",
    /* 19 */ "AMBULAN1.wav",
    /* 20 */ "FOUNTAIN.wav",
    /* 21 */ "GRILLOSZ.wav",
    /* 22 */ "HOJASZZZ.wav",
    /* 23 */ "FLASHZZZ.wav",
    /* 24 */ "CUCHI1ZZ.wav",
    /* 25 */ "KNRRRRRZ.wav",
    /* 26 */ "PHONE_02.wav",
    /* 27 */ "PHONE_03.wav",
    /* 28 */ "SSSHTZZZ.wav",
    /* 29 */ "BURGUER1.wav",
    /* 30 */ "FLIES_2Z.wav",
    /* 31 */ "PARRILLA.wav",
    /* 32 */ "WATER_2Z.wav",
    /* 33 */ "XIQUETZZ.wav",
    /* 34 */ "RONQUIZZ.wav",
    /* 35 */ "MOCO1ZZZ.wav",
    /* 36 */ "MOCO2ZZZ.wav",
    /* 37 */ "SPRINGZZ.wav",
    /* 38 */ "MARUJASZ.wav",
    /* 39 */ "ELECTROZ.wav",
    /* 40 */ "GLASS1ZZ.wav",
    /* 41 */ "OPDOORZZ.wav",
    /* 42 */ "CLDOORZZ.wav",
    /* 43 */ "FXH2ZZZZ.wav",
    /* 44 */ "BOTEZZZZ.wav",
    /* 45 */ "ELEC3ZZZ.wav",
};