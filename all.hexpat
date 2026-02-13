#pragma description Alfred Pelrock - ALFRED.1 Room Structure
#pragma endian little

import std.mem;
import std.core;
import std.string;

struct Pair {
    u32 offset;
    u32 size;
};


struct Color {
    u8 r;
    u8 g;
    u8 b;
} [[hex::inline_visualize("color", r * 4, g * 4, b *4 , 255)]];
struct Palette {
    Color colors[256];
} ;

struct Description {
    u8 start;
    u8 itemId;
    u8 say;
    u8 textColor;
    u8 index;
    u8 zero;
    char data[while(
        std::mem::read_unsigned($, 1) != 0xFD && std::mem::read_unsigned($, 1) != 0xF5
    )];
    u8 terminator;
};
// Variable-length text until control byte
// Variable-length text until control byte (0xFD)
struct ConvText {
    u8 text_bytes[while(
    std::mem::read_unsigned($, 1) != 0xFD && 
    std::mem::read_unsigned($, 1) != 0xF8 && 
    std::mem::read_unsigned($, 1) != 0xF4 &&
    std::mem::read_unsigned($, 1) != 0xF0)];
} [[sealed]];


struct DialogLine {
    u8 type;
    u8 idx;
    u8 colorIndicator;
    u8 color;
    u8 lineNumber;
    u8 separator;
    ConvText text;
    u8 end;
    if(end == 0xF8) {
        u8 action1;
        u8 action2;
    }
};
struct ThisAnimHeader {
    s16 x;                  // Bytes 0-1
    s16 y;                  // Bytes 2-3
    u8 w;                   // Byte 4
    u8 h;                   // Byte 5
    u16 stride;
    u8 numAnims;            // Byte 8
    u8 curAnimSequence;            // Byte 9
    u8 numFramesAnim1;      // Byte 10
    u8 numFramesAnim2;      // Byte 11
    u8 numFramesAnim3;      // Byte 12
    u8 numFramesAnim4;      // Byte 13
    u8 repeatAnim1;         // Byte 14
    u8 repeatAnim2;         // Byte 15
    u8 repeatAnim3;         // Byte 16
    u8 repeatAnim4;         // Byte 17
    u8 speedAnim1;          // Byte 18
    u8 speedAnim2;          // Byte 19
    u8 speedAnim3;          // Byte 20
    u8 speedAnim4;          // Byte 21
    u8 curFrameIndex;               // Byte 22
    u8 zorder;              // Byte 23
    u16 movementFlags1;     // Byte 24-25
    u16 movementFlags2;    // Byte 26-27
    u16 movementFlags3;   // Byte 28-29
    u16 movementFlags4;   // Byte 30-31
    u16 spriteExtra;   // Byte 32
 
    u8 action_flags;        // Byte 34
    u8 frameDelayCounter;
    u8 loopCount;
    u8 unusedPadding;
    u8 is_hotspot;          // Byte 38
    u8 disableAfterSequence;
    u8 unknown_39_to_43[4]; // Bytes 39-43
    
};

struct Hotspot {
    u8 type;
    u16 x;
    u16 y;
    u8 w;
    u8 h;
    u16 hotspotExtra;
};

struct Walkbox {
    u16 x;
    u16 y;
    u16 w;
    u16 h;
    u8 flags;

};

struct Exit {
    u16 targetRoom;
    u8 isEnabled;
    u16 x;
    u16 y;
    u8 w;
    u8 h;
    u16 targetX;
    u16 targetY;
    u8 dir;
};

fn min(s32 a, s32 b) {
    if (a > b)
        return b;
    else
        return a;
};

fn max(s32 a, s32 b) {
    if (a > b)
        return a;
    else
        return b;
};

struct Brick {
    s16 x;                  // Bytes 0-1
    s16 y;                  // Bytes 2-3
    u8 w;                   // Byte 4
    u8 h;                   // Byte 5
    u16 stride;
    u8 numAnims;            // Byte 8
    u8 unknown3;            // Byte 9
    u8 numFramesAnim1;      // Byte 10
    u8 numFramesAnim2;      // Byte 11
    u8 numFramesAnim3;      // Byte 12
    u8 numFramesAnim4;      // Byte 13
    u8 repeatAnim1;         // Byte 14
    u8 repeatAnim2;         // Byte 15
    u8 repeatAnim3;         // Byte 16
    u8 repeatAnim4;         // Byte 17
    u8 speedAnim1;          // Byte 18
    u8 speedAnim2;          // Byte 19
    u8 speedAnim3;          // Byte 20
    u8 speedAnim4;          // Byte 21
    u8 skipp;               // Byte 22
    u8 zorder;              // Byte 23
    u16 movementFlags1;     // Byte 24-25
    u16 movementFlags2;    // Byte 26-27
    u16 movementFlags3;   // Byte 28-29
    u16 movementFlags4;   // Byte 30-31
    u16 extra;   // Byte 32
    /*u16 movementFlagsAnim1;
    u16 movementFlagsAnim2;
    u16 movementFlagsAnim3;
    u16 movementFlagsAnim4;
    u8 unknown_30_to_32[3];     */      
    // Byte 33 (offset 0x21): Sprite type/layer - must be != 0xFF to be hotspot eligible
    u8 sprite_type;         // Byte 33
    // Byte 34 (offset 0x22): ACTION FLAGS bitmask
    // Bit 0 (0x01): Unknown action
    // Bit 1 (0x02): Unknown action
    // Bit 2 (0x04): Unknown action
    // Bit 3 (0x08): Unknown action
    // Bit 4 (0x10): TALK action available
    // Bit 5 (0x20): Unknown action
    // Bit 6 (0x40): Unknown action
    // Bit 7 (0x80): Unknown action
    u8 action_flags;        // Byte 34
    u8 unknown_35_to_37[3]; // Bytes 35-37 (3 bytes)
    // Byte 38 (offset 0x26): HOTSPOT FLAG
    // 0x00 = This sprite IS a clickable hotspot
    // 0x01 = This sprite is NOT a hotspot (decoration/non-interactive)
    u8 is_hotspot;          // Byte 38
    u8 unknown_39_to_43[1]; // Bytes 39-43
    // NOTE: Text descriptions indexed by combined order:
    // [selectable_sprites_in_order] + [static_hotspots_in_order]
    // NOT stored per-sprite! Position in list = text pointer index
};

struct RoomMetadata {
    
    u8 metadataPadding[5];
    u8 numAnims;
    u8 zeroes[92];
    
    u8 isRoom3 = (numAnims - 2) * 44 > 336;
    
    // Only define anims if numAnims > 2
    if (numAnims > 2) {
        if(isRoom3) {
            ThisAnimHeader anims[numAnims - 3];
            
            Brick brickAnim;
        } 
        else { 
            ThisAnimHeader anims[numAnims - 2];
        }
    }
    
    // Conditional padding based on room index or numAnims
    if (!isRoom3) {
        u8 zeroes2[336 - (numAnims - 2) * 44];
        padding[12];
    }

    u8 numExits;
    Exit exits[numExits];
    
    if (numExits * 14 <= 84) {
        u8 zeroes4[84 - numExits * 14];
    }
    
    u8 numWalkboxes;
    u16 scaleThresshold;
    u8 scaleDivisor;
    u8 scaleMode;
    Walkbox boxes[numWalkboxes];
    
    if (numWalkboxes * 9 <= 603) {
        u8 zeroes6[603 - numWalkboxes * 9];
    }
    
    u8 zeroes7[7];
    u8 numHotspots;
    u8 unknown2[1];
    Hotspot hotspots[numHotspots];
};


// Speaker IDs
enum SpeakerID : u8 {
    ALFRED = 0x0D,
    NPC = 0x20
};


struct Sound {
    u8 trackNumber;
    u8 roomFx[8];

};

struct Room {
    Pair pairs[13];
    u8 bg1[pairs[0].size] @pairs[0].offset;
    u8 bg2[pairs[1].size] @pairs[1].offset;
    u8 bg3[pairs[2].size] @pairs[2].offset;
    u8 bg4[pairs[3].size] @pairs[3].offset;   
    u8 bg5[pairs[4].size] @pairs[4].offset;
    u8 bg6[pairs[5].size] @pairs[5].offset;
    u8 bg7[pairs[6].size] @pairs[6].offset;
    u8 bg8[pairs[7].size] @pairs[7].offset;
    u8 spritePixelData[pairs[8].size] @pairs[8].offset;
    Sound sounds @pairs[9].offset;
    RoomMetadata metadata @pairs[10].offset;
    Palette palette @pairs[11].offset;
    //u8 texts[pairs[12].size] @pairs[12].offset;
    
   Description descriptions[while(
        $ < (pairs[12].offset + pairs[12].size) &&
        std::mem::read_unsigned($, 1) == 0xFF
    )] @pairs[12].offset;
    
    
    

    u32 descSize = sizeof(descriptions);
    u32 convSize = pairs[12].size - sizeof(descriptions);
    u32 convPos = pairs[12].offset + sizeof(descriptions);
    DialogLine lines[while(
        std::mem::read_unsigned($, 1) != 0xF5
    )] @ convPos;
   // u8 conversations[convSize] @(convPos);
   // ConversationElement elements[while($ < pairs[12].offset + pairs[12].size)] @(convPos);
    
};


//ThisAnimHeader room3anims[8] @0xEB57A;


Room rooms[55] @0x00000;

/*
struct Conversation {

DialogLine teapetece;
DialogLine nosecuando;
DialogLine completo;
DialogLine tarifa;
DialogLine bueno;
DialogLine todavia;
DialogLine calentamiento;
DialogLine nollego;
DialogLine frances;
DialogLine aunmucho;
DialogLine luzapagada;
DialogLine solo4000;
DialogLine tupones;
DialogLine notengo;
DialogLine novuelvas;
DialogLine losconque;
DialogLine chapa1;
DialogLine puesno;
DialogLine chapa2;
DialogLine mururoa;
DialogLine chapa3;
DialogLine fisica;
DialogLine chapa4;
DialogLine paranoverte;
DialogLine tutelopierdes;
DialogLine idiomas;
DialogLine griego;
DialogLine castidad;
DialogLine vicioso;
DialogLine ropa;
DialogLine pantalonescagados;
DialogLine princesa;
DialogLine maricon;
DialogLine hasconseguido;
DialogLine enello;
DialogLine perseverante;
DialogLine tamano;
DialogLine pequena;
};

Conversation conv @ 0xB21DE;


struct Guardia {
    DialogLine quedeseaCaballero;
    DialogLine entrarQuesiNo;
    DialogLine loSientoAbreALas9;
    DialogLine bonitaNoche;
    DialogLine enEfecto;
    DialogLine concepcionDeterminista;
    DialogLine cuestionInteresante;
    DialogLine vivimosAlienados;
    DialogLine noesLoMasGrave;
    DialogLine queEsNuestraDependenciaElectricidad;
    DialogLine NoExistenciaEfimera;
    DialogLine queEsNecesitarManosHumanas;
    DialogLine NoExistenciaEfimera2;
    DialogLine terceraDimension;
    DialogLine noSiga;
    DialogLine ustedDira;
    DialogLine casiSonLas9;
    DialogLine hastaLas9;
    DialogLine faltan5mins;
    DialogLine pesado;
    DialogLine porfavor;
    DialogLine deberAnteTodo;
    DialogLine comoMeEnfade;
    DialogLine jaQueMiedo;
    DialogLine lastima;
    DialogLine verguenza;
    DialogLine porfavor2;
    DialogLine no;
    DialogLine PORFAVOR3;
    DialogLine queNo;
    DialogLine vaVenga;
    DialogLine estabien;
};

Guardia g@ 0x127484;


struct Travel1 {
    DialogLine leVeoBlanco;
    DialogLine noEsPorElSol;
    DialogLine cancun;
    DialogLine nomeinteresaSol;
    DialogLine estaDeEnhorabuena;
    DialogLine enQueConsiste;
    DialogLine empresaGarantiza;
    DialogLine proximoJuego;
    DialogLine comoQuiera;
    DialogLine noMeGustaSol;
    DialogLine cansarmeDeUsted;
    DialogLine rataAlbufera;
    DialogLine vuelvaCuando;
};

struct Travel2 {
    DialogLine digame;
    DialogLine conocerEgipto;
    DialogLine fantasticaIdea;
    DialogLine excesivo;
    DialogLine unicaAgencia;
    DialogLine noTengoDineor;
    DialogLine hermanaCaridad;
    DialogLine regatear;
    DialogLine guardeloParaEgipto;
    DialogLine queHacesEstaNoche;
    DialogLine dormir;
};

struct Travel3 {
    DialogLine conocerEgipto;
    DialogLine solo200000;
    DialogLine noTengoEseDinero;
    DialogLine deCuantoDispone;
    DialogLine de150000;
    DialogLine hummm;
    DialogLine ahoraQueRecuerdo;
    DialogLine aprendices;
    DialogLine noSeAsuste;
    DialogLine enfin;
    DialogLine felizViaje;
    DialogLine siClaro;
    DialogLine unicaOpcion;
    DialogLine caraDura;
    DialogLine muybienFelizViaje;
    DialogLine podriaAndando;
    DialogLine tanViejo;
    DialogLine tieneRazon;
    DialogLine felizViaje3;
    DialogLine autostop;
    DialogLine conEsaCara;
    DialogLine tieneRazon2;
    DialogLine felizViaje4;
    DialogLine ademasDeDormir;
    DialogLine sonar;
};

struct Travel {
    Travel1 t1;
    Travel2 t2;
    Travel3 t3;
};

Travel t@ 0x3754BE;

struct Moros {
    DialogLine lines[while(
        std::mem::read_unsigned($, 1) != 0xF5
    )];
};

struct Estatuas {
    DialogLine lines[while(
        std::mem::read_unsigned($, 1) != 0xF5
    )];
};

Moros moros @ 0x3F2960;
Estatuas estatuas @ 0x14DBA3;*/