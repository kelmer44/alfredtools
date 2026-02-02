#pragma description Alfred Pelrock - ALFRED.7 Structure
#pragma endian little
#pragma array_limit 100000

import std.mem;
import std.core;
import std.string;


struct Color {
    u8 r;
    u8 g;
    u8 b;
} [[hex::inline_visualize("color", r * 4, g * 4, b *4 , 255)]];
struct Palette {
    Color colors[256];
} ;


struct RleChunk {
    u8 pixelData[while(
           !std::mem::eof() &&                        
           std::mem::read_string($, 4) != "BUDA"  )
       ];
   char marker[4];
};


RleChunk cuadroCama[8] @ 0x00; // verified
Palette palCuadro @ 0x7984; //verified
u8 unknown0[0x144] @ 0x7C84;
u8 largeFontData[4800] @ 0x7DC8; //verified
u8 alfredElectrocuta1[11745] @ 37000; // verified
u8 unknownbetweenalfreds[0x2F] @ 0xBE69;
u8 alfredElectrocuta2[4312] @ 48792; // verified
u8 alfredElectrocuta3[9512] @ 53106; // verified
u8 unknownAfterElectrocuta[0x1414] @ 0xF49A;
RleChunk alfredCombRight @ 0x108AE; //verified
RleChunk alfredCombLeft @ 0x15958; //verified
RleChunk computer[8] @ 0x1A9EE; //verified
Palette palComputer @ 198050; //verified
// buda 17
u8 unknownAntesLibros[0x13E] @ 0x308A2;
u8 libros[0x3526] @ 0x309E0; //verified
RleChunk unknownBuda @ 0x33F06;

RleChunk pareja @ 236645; // verified
RleChunk faraonCamina @ 261449; // verified
RleChunk faraonLevantaMano @ 280359; // verified
RleChunk pareja2 @ 298589; // verified
RleChunk guardia @ 341229; // verified
RleChunk chicaSeLava @ 360835; //verified
RleChunk llamita @ 381449; // verified
RleChunk chicaSeLava2 @ 381825; //verified
RleChunk reloj @ 397665; // verified

RleChunk alfredCama @ 398563; //verified

u8 entreCamaYCirculo[1702] @ 409885;
RleChunk alfredCirculo[4] @ 411587; //verified
RleChunk receta[8] @ 457677; // verified
Palette palReceta @ 505521;//verified

u8 afterPalReceta[95] @ 0x7B9B1;
// buda 48
RleChunk periodico[8] @ 506385; //verified
Palette palPreiodico @ 558013; //verified
RleChunk chafarderError @ 0x886BD; // verified
RleChunk alfredLibro @ 578943; //verified
RleChunk thinkingBalloon @ 598051; //verified

RleChunk tabla[8] @ 598907; // verified!
Palette palTabla @ 724711; // verified
RleChunk mapa[8] @ 725485; //verified
Palette palMapa @ 909329; // verified
RleChunk menu[8] @ 910093; // verified
Palette menuPalette @ 1038141; // verified
u8 codeSnippet[0x2A0] @ 0xFDA3D;
u8 cursor1[288] @ 0x0FDDFD; //verified
u8 cursor2[288] @ 0x0FDCDD; // verified
u8 cursor3[288] @ 0x0FDF1D; // verified
Palette paletteBetweenCursors @ 0xFE03D; //verified
u8 cursor4[288] @ 0x0FE33D; // verified
u8 cursor5[288] @ 0x367EF0; // verified
RleChunk unknownBuda76 @ 1041501; //verified

RleChunk cuadradoMenu @ 1042757; //verified

u8 beforeTetas[0x64] @ 0xFFBE3; //verified
RleChunk libroTetas[8] @ 1047623; //verified
Palette palLibroTetas @ 1147081; //verified
RleChunk otroLibro[8] @ 1147845; //verified
Palette palOtroLibro @ 1267955; //verified
RleChunk simbolos @ 1268719; //verified
RleChunk unknown1 @ 1341235; // verified
RleChunk unknown2 @ 1347767; //verified
// buda 97

u8 englishBookTitles[0x3519] @ 0x14C53F; // verified
RleChunk actionBalooons1 @ 1374808; //verified
RleChunk cuadroOk[8] @ 1387144; //98-105
Palette palCuadroOk @ 1425352; //106
RleChunk alfredCama2 @ 1426116; //106

Palette palRoom28 @ 0x1610CE;
RleChunk nadadoras @ 1446862;
RleChunk tiposBebiendo @ 1473364;
RleChunk tiposBebidos @ 1512060;
RleChunk smoke @ 1526432;
RleChunk cocodrilo @ 1556540; // 111
RleChunk trampilla @ 1583706;

u8 alfredHablaObreros[148464] @ 1600956; // 208 width
RleChunk alfredTrampilla @  1749420; //95 width

RleChunk alfredClimbing @ 1761234;
RleChunk alfredClimbing2 @ 1766378;

u8 alfredSaleTrampilla @ 0x1B02D4;
RleChunk alfredMunheco1 @ 2060922; //incomplete!
RleChunk alfredMunheco2 @ 2115632;
RleChunk balloon @2176936;
RleChunk iconosMusica @ 2201882;
RleChunk iconoAltavoz @ 2208286;
RleChunk iconoMusic @2210448;
RleChunk iconoFX @2212846;
RleChunk blankGUI @ 2214708;
RleChunk musicPlayer @ 2214760; // two sizes

RleChunk black[8] @ 2227418;
Palette somePalette @ 2229480;
RleChunk alfredFight @ 2230266;
RleChunk otrolibro[8] @ 2253656;
Palette otrolibroPalette @ 2284678;
RleChunk unknown @ 2285446;
RleChunk alfredCama4 @2285694; //144
RleChunk censored[8] @2306538;
Palette censoredPalette @ 2321060;
RleChunk code @ 2321828; //153
RleChunk code2 @ 2361388;
RleChunk artwork @ 2381082;

u8 settingsMenu12[65536] @ 2405266;
RleChunk settingsMenuRLE3 @ 2470802;
u8 settingsMenu4[32768] @  2500216;
RleChunk settingsMenuRLE5 @ 2532984;
u8 settingsMenu67[92160] @ 2563266;

Palette settingsMenuPalette @ 2655426;

RleChunk soundControls2[4] @ 2662588; //159
RleChunk code3 @ 2669050;
RleChunk code4 @ 2688168;
RleChunk discoAlfred[8] @ 2727564;
Palette discoAlfredPal @ 2833276;
RleChunk pergamino[8] @ 2834044;
Palette pergaminoPalette @ 2971800;
RleChunk alfredDescamisa @ 2972568; //181
RleChunk overlayMapa @ 2980872;
RleChunk humo2 @ 3006794;
RleChunk flechas @ 3037008;
RleChunk alfredCama34234 @ 3038454;
RleChunk conChica[8] @ 3058226;
Palette conChicaPalette @ 3185280; //194
u8 flechitas[1300] @ 3186048; //+772; witdh = 20
u8 flechitas2[8100] @ 3186048 + 1300; // width = 28
u8 othericons[26798] @ 3195448; // 3186048 + 1300 + 8100;
RleChunk piernas @ 3222246; //multiple sizes
u8 unknownimage[256000] @ 3271454;
RleChunk credits @ 3527454;