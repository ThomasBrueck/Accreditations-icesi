from django.core.mail import send_mail

def sendEmailCode(user, code):

        try:
            send_mail(
                "Codigo de verificacion de sistema de acreditacion", 
                f"Your verification code is: {code}",
                'acreditacionesicesi@gmail.com',
                [user.email],
                fail_silently=False
            )

        except Exception as e:
            print(f"Error al enviar codigo al correo {user.email}: {e}") 