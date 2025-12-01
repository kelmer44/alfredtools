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

// buda 76

RleChunk cuadradoMenu @ 1042757;

RleChunk libroTetas[8] @ 1047623;
Palette palLibroTetas @ 1147081;
RleChunk otroLibro[8] @ 1147845;
Palette palOtroLibro @ 1267955;
RleChunk simbolos @ 1268719;
RleChunk unknown1 @ 1341235;
RleChunk unknown2 @ 1347767;
// buda 97

RleChunk cuadroOk[8] @ 1387148;
Palette palCuadroOk @ 1425352;
RleChunk alfredCama2 @ 1426116;

Palette palRoom28 @ 0x1610CE;
RleChunk nadadoras @ 1446862;
RleChunk tiposBebiendo @ 1473364;
RleChunk tiposBebidos @ 1512060;
RleChunk smoke @ 1526432;
RleChunk cocodrilo @ 1556540;
RleChunk trampilla @ 1583702;

// buda 113