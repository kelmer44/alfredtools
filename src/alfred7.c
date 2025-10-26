// #include <stdio.h>
// #include <stdlib.h>
// #include <memory.h>
// #include "lodepng.h"
// #include "functions.h"



// int count = 0;
// int written = 0;

// unsigned int index2=0;
// //212743
// unsigned int index=0x0031eb1e;//0x00182a56;//0x00174aa0;//0x152a88;//0x922cb+176;//0x9392b;//
// int w=51;
// int h=102;
// unsigned int offset;

// unsigned char getExtraCharacters(unsigned char t)
// {
// 	unsigned char ex[]=
// 	{
// 		0x80,0x82,0x83,0x7b,0x7c,0x7d,0x7e,0x7f,0xc8,0xad,1,2
// 	};
// 	unsigned char cex[]=
// 	{
// 		'�','�','�','�','�','�','�','�',' ','�',' ',' '
// 	};

// 	unsigned char ret=t;
// 	for (int i=0;i<12;i++)
// 	{
// 		if (t==ex[i])
// 		{
// 			ret=cex[i];
// 			break;
// 		}
// 	}

// 	return ret;
// }

// void checkChar(unsigned char *buf2,int size)
// {

// 	for (int i=0;i<size;i++)
// 	{
// 		buf2[i]=getExtraCharacters(buf2[i]);
// 	}
// }


// int extractAlfred7(int argc, char *argv[])
// {
//     unsigned char *pic=(unsigned char *)malloc(307200*100);

// 	// QCoreApplication a(argc, argv);



// 	int jj=0;


// 	argc=2;
// 	argv[1]="C:/compartido/alfred/alfred.7";

// 	FILE *fp1=fopen(argv[1],"rb");


// 	fseek(fp1, 0L, SEEK_END);
// 	int size = ftell(fp1);
// 	fseek(fp1, 0L, SEEK_SET);

// 	unsigned char *bufferFile=(unsigned char *)malloc(size);
// 	fread(bufferFile, 1, size, fp1);




// 	unsigned char *buf2=(unsigned char *)malloc(56);
// 	unsigned int lofsset=199136;

// 	fseek(fp1, lofsset, 0);

// 	for (int l=0;l<126;l++)
// 	{

// 		memset(buf2,0,56);
// 		fread(buf2,1,55,fp1);
// 		checkChar(buf2,56);
// 		printf("%s\n",buf2);

// 		memset(buf2,0,56);
// 		fread(buf2,1,30,fp1);
// 		checkChar(buf2,56);
// 		printf("%s\n",buf2);

// 		memset(buf2,0,56);
// 		fread(buf2,1,23,fp1);
// 		checkChar(buf2,56);
// 		printf("%s\n",buf2);

// 		l+=0;


// 	}

// 	exit(0);




// 	if (argc!=2)
// 	{
// 		printf(" uso: test fichero");
// 	}
// 	else
// 	{




// 		int blok=0;
// 		//index=0x1a9ee;
// 		unsigned int index2=0;
// 		int i=0;
// 		int j=0;

// 		w=100;//-202;//90-26;
// 		h=90;//-42;//120-23;
// 		//offset=(60*51*102);
// 		int nframes=3;


// 	unsigned int indexb=index;
// 		while (j<90)
// 		{

// 			//while (bufferFile[index]==0)
// 			//	index++;

// 			/*

// 			while ((bufferFile[index2]!='B') || (bufferFile[index2+1]!='U') || (bufferFile[index2+2]!='D') || (bufferFile[index2+3]!='A'))
// 				index2++;

// 			unsigned int sizeBlock=(index2-index);

// 			index2+=4;

// 			printf("bloque = %d, size = %d\n",i,sizeBlock);
// 			i++;
// 			index=index2;

// 			*/

// 			//if (j==8)
// 			//{
// 			//	index+=768;
// 			//}




// 			if ((bufferFile[index]=='B') && (bufferFile[index+1]=='U') && (bufferFile[index+2]=='D') && (bufferFile[index+3]=='A'))
// 			{

// 				blok++;
// 				if (blok==1)// || (index2>=256000))
// 				{


// 				QImage *image=new QImage(640,468,QImage::Format_Indexed8);
// 				//QImage *image=new QImage(w*nframes,h,QImage::Format_Indexed8);



// 				unsigned char *bufferPaleta=getPalette();

// 				bool kk;
// 				int index3=0;
// 		unsigned int superancho,frame,sx,sy,total;
// 		total=w*h;
// 		superancho=w*n;

// 				for (int y=0;y<468;y++)
// 				{
// 					for (int x=0;x<640;x++)
// 					{
// 						image->setPixel(x,y,pic[index3++]);
// 				//frame=x/w;
// 				//sy=y;
// 				//sx=x-(frame*w);
// 				//image->setPixel(x,y,pic[(frame*total)+(sy*w)+sx]);
// 					}
// 				}

// 				QString pp("C:/proyectos/test7/debug/kk");//.png");

// 				char buff[3];
// 				memset(buff,0,3);

// 			itoa(j,buff,10);
// 			pp.append(QString(buff));
// 			pp.append(".png");
// 			j++;


// 				kk=image->save(pp,"PNG");



//  				index2=0;
// 				memset(pic,0,307200*100);
// 				}
// 				else
// 					index2++;

// 				index+=4;

// 				//index2=((blok)*(32768));


// 			//index=indexb;
// 			//index2=0;
// 			//w-=1;
// 			//h-=1;


// 			}
// 			else
// 			{


// 				pic[index2]=bufferFile[index];
// 				index2++;
// 				index++;


// 				/*
// 				unsigned char count=bufferFile[index];
// 				unsigned char color=bufferFile[index+1];
// 				unsigned int k;
// 				for (k=index2;k<index2+count;k++)
// 					pic[k]=color;

// 				pic[k]=(unsigned char)color;

// 				index2+=count;
// 				index+=2;
// 				*/

// 			}



// 		}

// 	}

// 	exit(0);


// }
