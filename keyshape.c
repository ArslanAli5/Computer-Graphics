#include<GL/Glut.h> //includes the opengl, glu, and glut header files
#include<stdlib.h> //includes the standard library header file
#include <windows.h>  // for MS Windows
#include <GL/glut.h>  // GLUT, include glu.h and gl.h
#include <math.h>
int chooice = 0;
 /* Initialize OpenGL Graphics */
void initGL() {
    glClearColor(1, 1, 1, 0);
}

static void Key(unsigned char key, int x, int y)
{
    if (key == 'T' || key == 't')
    {
        //glClearColor(1, 1, 1, 0);
        chooice = 1;
    }
    else if (key == 'C' || key == 'c')
    {
        //glClearColor(1, 1, 1, 0);
        chooice = 2;
    }
    else if (key == 'r' || key == 'R')
    {
        //glClearColor(1, 1, 1, 0);
        chooice = 3;
    }
}
void display(void)
{
    glMatrixMode(GL_PROJECTION);// sets the current matrix to projection
    glLoadIdentity();//multiply the current matrix by identity matrix
    glClear(GL_COLOR_BUFFER_BIT);
    if (chooice == 1 )
    {      
        glBegin(GL_TRIANGLES);
        glColor3f(0.6, 0.3, 0);
        glVertex2f(0, 1);
        glVertex2f(-0.5, 0);
        glVertex2f(0.5, 0);
        glEnd();
    }
    else if(chooice== 2)
    {
        float theta;
        glColor3f(0.6, 0.3, 0);
        glBegin(GL_POLYGON);
        for (int i = 0; i < 360; i++)
        {
            theta = i * 3.14 / 180;
            glVertex2f(0.5 * cos(theta), 0.5 * sin(theta));
        }
        glEnd();
    }
    else if (chooice==3)
    {
        glBegin(GL_POLYGON);
        glColor3f(0.6, 0.3, 0);
        glVertex2f(-0.9, 0.50);
        glVertex2f(-0.9, -0.50);
        glVertex2f(0.9, -0.50);
        glVertex2f(0.9, 0.5);
        glEnd();
    }
    glFlush();
}

int main(int argc, char** argv)
{
    glutInit(&argc, argv);
    glutInitWindowSize(500, 500);   //sets the width and height of the window in pixels
    glutInitWindowPosition(10, 10);//sets the position of the window in pixels from top left corner 
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);//creates a single frame buffer of RGB color capacity.
    glutCreateWindow("SP19-BCS-103");//creates the window as specified by the user as above.
    glClearColor(1, 1, 1, 0); // sets the backgraound color to white light
    glClear(GL_COLOR_BUFFER_BIT); // clears the frame buffer and set values defined in glClearColor() function call 
    initGL();
    glutDisplayFunc(display);//links the display event with the display event handler(display)
    glutKeyboardFunc(Key);
    glutMainLoop();//loops the current event
}

