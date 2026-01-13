# create_test_users.py
# Script para crear usuarios de prueba con diferentes roles

from django.contrib.auth.models import User
from users.models import DoctorProfile

def create_test_users():
    """
    Crea usuarios de prueba para el sistema:
    - Admin: admin / admin123
    - Doctor: doctor / doctor123
    - Paciente: paciente / paciente123
    """
    
    # 1. Crear Admin
    print("Creando usuario Admin...")
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@clinica.com',
            password='admin123',
            first_name='Carlos',
            last_name='Admin'
        )
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        
        DoctorProfile.objects.create(
            user=admin_user,
            role='ADMIN'
        )
        print("✅ Usuario Admin creado correctamente")
    else:
        print("⚠️ Usuario Admin ya existe")
    
    # 2. Crear Doctor
    print("\nCreando usuario Doctor...")
    if not User.objects.filter(username='doctor').exists():
        doctor_user = User.objects.create_user(
            username='doctor',
            email='doctor@clinica.com',
            password='doctor123',
            first_name='María',
            last_name='González'
        )
        
        DoctorProfile.objects.create(
            user=doctor_user,
            role='DOCTOR',
            license_number='MD-12345',
            specialization='Medicina General'
        )
        print("✅ Usuario Doctor creado correctamente")
    else:
        print("⚠️ Usuario Doctor ya existe")
    
    # 3. Crear Paciente
    print("\nCreando usuario Paciente...")
    if not User.objects.filter(username='paciente').exists():
        patient_user = User.objects.create_user(
            username='paciente',
            email='paciente@clinica.com',
            password='paciente123',
            first_name='Juan',
            last_name='Pérez'
        )
        
        DoctorProfile.objects.create(
            user=patient_user,
            role='PATIENT',
            phone='0999123456'
        )
        print("✅ Usuario Paciente creado correctamente")
    else:
        print("⚠️ Usuario Paciente ya existe")
    
    print("\n" + "="*50)
    print("✅ Usuarios de prueba creados exitosamente")
    print("="*50)
    print("\n📋 Credenciales de prueba:")
    print("\n1. ADMIN:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n2. DOCTOR:")
    print("   Username: doctor")
    print("   Password: doctor123")
    print("\n3. PACIENTE:")
    print("   Username: paciente")
    print("   Password: paciente123")
    print("\n" + "="*50)

if __name__ == '__main__':
    create_test_users()
