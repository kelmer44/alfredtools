
// #include <stdio.h>
// #include <stdlib.h>
// #include <memory.h>
// #include "lodepng.h"
// #include "functions.h"

// int n;
// int count = 0;
// int written = 0;

// unsigned int index2 = 0;
// int w = 102;
// int h = 51;
// unsigned int offset;

// int extractAlfred9()
// {
//     unsigned char *pic = (unsigned char *)malloc(640 * 480 * 600);

//     QCoreApplication a(argc, argv);

//     // for (int jj=1;jj<50;jj++)
//     //{

//     // int jj=0;
//     // w=130;
//     // h=55;
//     // offset=(60*51*102);
//     // int nframes=18;

//     /*
//         int jj=0;
//         w=51;
//         h=102;
//         offset=0;
//         int nframes=60;
//     */

//     FILE *fp1 = fopen("files/alfred.9", "rb");

//     fseek(fp1, 0L, SEEK_END);
//     int size = ftell(fp1);
//     fseek(fp1, 0L, SEEK_SET);

//     unsigned char *bufferFile = (unsigned char *)malloc(size);
//     fread(bufferFile, 1, size, fp1);

//     unsigned int index = 0;
//     int blok = 0;
//     index = 0; // 0x00186dbc;//0x15c2c8;//0x14fa66;//578943;//0x6411d+1702;//0x6411d;//0x67389;//0x6411d;
//     int iIndex = index;
//     // bool nextBuda=false;
//     int counter;

//     while (index < size) // size)
//     {

//         // while (bufferFile[index]==0)
//         //	index++;

//         // if ((bufferFile[index]=='B') && (bufferFile[index+1]=='U') && (bufferFile[index+2]=='D') && (bufferFile[index+3]=='A'))
//         {
//             /*
//             if (nextBuda==true)
//             {

//                 counter--;
//                 if (counter==0)
//                     break;
//             }
//             */
//             /*
//             index+=4;
//             blok++;
//             index2++;
//             //if (blok==30)
//             {

//                 break;
//                 blok=0;
//                 //index+=768;
//                 //nextBuda=true;
//                 counter=2;
//             }
//             */
//         }
//         // else
//         {

//             pic[index2] = bufferFile[index];
//             index2++;
//             index++;

//             /*
//             unsigned char count=bufferFile[index];
//             unsigned char color=bufferFile[index+1];
//             unsigned int k;
//             for (k=index2;k<index2+count;k++)
//                 pic[k]=color;

//             index2+=count;

//             index+=2;
//             */
//         }
//     }

//     // int alto=(index2-iIndex)/640;
//     // QImage *image=new QImage(640,400,QImage::Format_Indexed8);
//     unsigned int superancho, frame, sx, sy, total;
//     w = 51;
//     h = 102;
//     offset = 0; //(60*51*102);
//     int nframes = 11;
//     total = w * h;



//     // superancho=w*n;
//     QImage *image = new QImage(640, 8, QImage::Format_Indexed8);

//     unsigned char *palette = getPalette();

//     image->setColorCount(256);
//     image->setColorTable(*ctable);

//     int index3 = 0;

//     // int frame;

//     for (int y = 0; y < 8; y++)
//     {
//         for (int x = 0; x < 640; x++)
//         {
//             image->setPixel(x, y, pic[index3++]);
//             /*
//             frame=x/w;
//             sy=y;
//             sx=x-(frame*w);
//             image->setPixel(x,y,pic[(offset)+(frame*total)+(sy*w)+sx]);
//             */
//         }
//     }

//     bool kk;

//     char buff[3];
//     memset(buff, 0, 3);
//     QString pp("C:/proyectos/test7b/debug/kk.png");
//     kk = image->save(pp, "PNG");

//     exit(0);
// }
