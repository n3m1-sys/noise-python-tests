p = [151,160,137,91,90,15,
   131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,
   190, 6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,
   88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,
   77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,
   102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,
   135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,
   5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,
   223,183,170,213,119,248,152, 2,44,154,163, 70,221,153,101,155,167, 43,172,9,
   129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,
   251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,
   49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,
   138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]

def perlin(x,y,z):
    '''
    Función principal Perlin

    INPUT: (x,y,z) es un vector de números reales de un punto dentro de un cubo.
    OUTPUT: Un número real.
    '''

    # Calculamos el cubo unidad que contiene el punto (x,y,z).
    # (xi,yi,zi) serán las coordenadas (x0,y0,z0) del cubo.
    
    xi = int(x) & 255
    yi = int(y) & 255
    zi = int(z) & 255
    
    # Calculamos el punto relativo a (x,y,z) dentro de un cubo de aristas de 1.0.
    # (xf,yf,zf) tendrán la parte decimal de (x,y,z).

    xf = x - float(xi)
    yf = y - float(yi)
    zf = z - float(zi)

    # Calculamos las curbas de suavizado para cada uno de los puntos de las 
    # coordenadas (x,y,z) y las guardamos en (u,v,w).

    xfade = fade(xf)
    yfade = fade(yf)
    zfade = fade(zf)

    # Hasheamos las 8 coordenadas de de la unidad cubo segun la permutación p con la que estamos trabajando.
    # Las coordenadas de los vertices van tal que el hash de (x0,y0,z0) sería la variable aaa y (x1,y1,z1) sería la variable bbb.
    # La función hash en este caso consiste en escoger valores de la permutación, en función de las coordenadas minimas del cubo.

    aaa = p[(p[(p[ xi   %256]+ yi   )%256]+ zi   )%256]
    aab = p[(p[(p[ xi   %256]+ yi   )%256]+(zi+1))%256]
    aba = p[(p[(p[ xi   %256]+(yi+1))%256]+ zi   )%256]
    abb = p[(p[(p[ xi   %256]+(yi+1))%256]+(zi+1))%256]
    baa = p[(p[(p[(xi+1)%256]+ yi   )%256]+ zi   )%256]
    bab = p[(p[(p[(xi+1)%256]+ yi   )%256]+(zi+1))%256]
    bba = p[(p[(p[(xi+1)%256]+(yi+1))%256]+ zi   )%256]
    bbb = p[(p[(p[(xi+1)%256]+(yi+1))%256]+(zi+1))%256]

    # Realizamos la interpolación de los 8 vertices

    x1 = lerp(xfade,grad(aaa,xf  ,yf  ,zf  ),
                    grad(baa,xf-1,yf  ,zf  ))
    x2 = lerp(xfade,grad(aba,xf  ,yf-1,zf  ), 
                    grad(bba,xf-1,yf-1,zf  ))
    y1 = lerp(yfade,x1, x2)
    x1 = lerp(xfade,grad(aab,xf  ,yf  ,zf-1), 
                    grad(bab,xf-1,yf  ,zf-1))
    x2 = lerp(xfade,grad(abb,xf  ,yf-1,zf-1), 
                    grad(bbb,xf-1,yf-1,zf-1))
    y2 = lerp(yfade,x1,x2)
    
    return (lerp(zfade,y1,y2)+1)/2


def fade(t):
    '''
    Se encarga de suavizar las interpolaciones lineales

    INPUT: t es un número real entre 0.0 y 1.0.
    OUTPUT: Un número real entre 0.0 y 1.0, solución de la ecuación: 6t⁵-15t⁴+10t³.
    '''
    return t * t * t * (t * (t * 6 - 15) + 10)


def lerp(t,a,b):
    '''
    Realiza una interpolación lineal con parametro alpha = t

    INPUT: t, a y b son 3 números reales entre 0.0 y 1.0
    OUTPUT: Un número real entre 0.0 y 1.0
    '''
    # La ecuación a + t * (b - a) puede no ser precisa, ya que no garantiza que lerp(t=1,a,b)=b por errores aritmeticos con coma flotante
    return (1 - t) * a + t * b  

def grad(hash, x, y, z):
    '''
    Escoge un vector gradiente entre la siguiente lista en función de los 4 bits menos significativos de hash:
        [(1,1,0),(-1,1,0),(1,-1,0),(-1,-1,0),
         (1,0,1),(-1,0,1),(1,0,-1),(-1,0,-1),
         (0,1,1),(0,-1,1),(0,1,-1),(0,-1,-1)]
    Y realiza el producto escalar por el vector de dirección definido por (x,y,z)

    INPUT: hash es un número entero entre 0 y 255, (x,y,z) son 3 números reales
    OUTPUT: Un número real

    La siguiente tabla muestra como se escoge el gradiente en función del hash:

     h = hash & 0xF | vector gradiente aleatorio
    ----------------+----------------------------
         0b0000     |         ( 1, 1, 0)
         0b0001     |         (-1, 1, 0)
         0b0010     |         ( 1,-1, 0)
         0b0011     |         (-1,-1, 0)
         0b0100     |         ( 1, 0, 1)
         0b0101     |         (-1, 0, 1)
         0b0110     |         ( 1, 0,-1)
         0b0111     |         (-1, 0,-1)
         0b1000     |         ( 0, 1, 1)--
         0b1001     |         ( 0,-1, 1)-+--
         0b1010     |         ( 0, 1,-1)-+-+--
         0b1011     |         ( 0,-1,-1)-+-+-+--     Estos vectores tienen más probabilidades de ser elegidos
         0b1100     |         ( 0, 1, 1)-- | | |     ya que hay más hashes que los pueden escoger.
         0b1101     |         ( 0,-1, 1)---- | |
         0b1110     |         ( 0, 1,-1)------ |
         0b1111     |         ( 0,-1,-1)--------

    '''
    h = hash & 0xF                              # Máscara '0b1111' para utilizar los 4 bits menos significativos, de esta forma: 0 <= h <= 15.
                                                # Otra forma de hacer esto sería realizar congruencias modulo 16 sobre hash cada vez que analizamos h,
                                                # es decir, h = hash % 16

    u = (x if h < 8 else y)                     # Si el bit más significativo es 0 entonces u = x, si no u = y
    if h < 4:                                   # Si los dos bits menos significativos son 0 v = y
        v = y
    elif h == 12 or h == 14:                    # Si los dos bits más significativos son 1 y el bit menos significativo es 0 (0b1100 = 12 or 0b1110 = 14) v = x
        v = x
    else:                                       # Para el resto de casos v = z
        v = z
                                                                        # Si el bit menos significativo es 0 u es positivo y si no es negativo
    return (u if h & 0b1 == 0 else -u)+(v if h & 0b10 == 0 else -v)     # Si el segundo bit menos significativo es 0 v es poitivo y si no es negativo

print(perlin(4.8, 5.3, 7.2))