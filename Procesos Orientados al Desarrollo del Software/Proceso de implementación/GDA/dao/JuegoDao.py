from Conexion import Sesion
from datos.Juego import Juego


class JuegoDao:

    def iniciarOperacion(self):

        try:
            sesion = Sesion()  # iniciar sesion con la bd
        except MySQLdb.OperationalError:
            print "Error en la conexion"
            sesion = None

        return sesion

    def agregar(self, juego):
        sesion = self.iniciarOperacion()

        cursor = sesion.obtenerCursor()
        try:
            cursor.execute("""insert into Juego(nombre,descripcion)
              values('%s', '%s')""" % (juego.getNombre(), juego.getDescripcion()))
            sesion.commit()
        except:
            print "Error en ejecucion de la query"
            sesion.getEstado().rollback()  # volver al estado anterior

        finally:
            cursor.close()
            sesion.cerrarConexion()

    def eliminar(self, juego):
        sesion = self.iniciarOperacion()

        cursor = sesion.obtenerCursor()
        try:
            cursor.execute("""delete Juego from Juego where Juego.idJuego='%s'""" % (juego.getId()))
            sesion.commit()
        except:
            print "Error, no se pudo eliminar"
            sesion.getEstado().rollback()
        finally:
            cursor.close()
            sesion.cerrarConexion()

    def traerJuego(self, nombre):
        sesion = self.iniciarOperacion()
        cursor = sesion.obtenerCursor()
        juego = None
        try:
            cursor.execute("""select * from Juego where Juego.nombre='%s'""" % nombre)
            resultado = cursor.fetchone()
            if resultado is not None:
                juego = Juego(resultado[1], resultado[2])
                juego.setId(resultado[0])
        except:
            print "Error, no se pudo traer el juego"
        finally:
            cursor.close()
            sesion.cerrarConexion()

        return juego

juego = JuegoDao()
print juego.traerJuego("fornite")
