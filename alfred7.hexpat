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


RleChunk cuadroCama[8] @ 0x00;
Palette palCuadro @ 0x7984;

u8 largeFontData[4608] @ 0x7DC8;
RleChunk alfredCombRight @ 0x108AE;
RleChunk alfredCombLeft @ 0x15958;
RleChunk computer[8] @ 0x1A9EE;
Palette palComputer @ 198050;
// buda 17

RleChunk pareja @ 236645;
RleChunk faraonCamina @ 261450;
RleChunk faraonLevantaMano @ 280359;
RleChunk pareja2 @ 298589;
RleChunk guardia @ 341229;
RleChunk chicaSeLava @ 360832;
RleChunk llamita @ 381450;
RleChunk chicaSeLava2 @ 381826;
RleChunk reloj @ 397666;
RleChunk alfredCama @ 398559;


RleChunk alfredCirculo[4] @ 411587;

RleChunk receta[8] @ 457673;
Palette palReceta @ 505521;
// buda 48
RleChunk periodico[8] @ 506385;
Palette palPreiodico @ 558917;
RleChunk alfredLibro[2] @ 559681;
RleChunk thinkingBalloon @ 598051;

RleChunk tabla[8] @ 598907; // uncertain!
Palette palTabla @ 724711;
RleChunk mapa[8] @ 725485;
Palette palMapa @ 909329;
RleChunk menu[8] @ 910093;
Palette menuPalette @ 1038141;
// buda 76
u8 cursor1[288] @ 0x0FDDFD;

u8 cursor2[288] @ 0x0FDCDD;

u8 cursor3[288] @ 0x0FDF1D;

u8 cursor4[288] @ 0x0FE33D;

u8 cursor5[288] @ 0x367EF0;


  

RleChunk cuadradoMenu @ 1042757;

RleChunk libroTetas[8] @ 1047623;
Palette palLibroTetas @ 1147081;
RleChunk otroLibro[8] @ 1147845;
Palette palOtroLibro @ 1267955;
RleChunk simbolos @ 1268719;
RleChunk unknown1 @ 1341235;
RleChunk unknown2 @ 1347767;
// buda 97

RleChunk cuadroOk[8] @ 1387148; //98-105
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


// buda 113
u8 englishBookTitles[0x3519] @ 0x14C53F;