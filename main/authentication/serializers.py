from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class My_TokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        mytoken = super().get_token(user)
        return mytoken
    
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields =  ['email', 'user_name', 'surname', 'first_name', 'last_name', 
                   'is_doctor', 'is_medical_staff', 'is_final_authority', 'password', 'password2']
        extra_kwargs ={
            'password':{'write_only': True}
        }
    
    def save(self):
        user_name = self.validated_data['user_name']
        surname = self.validated_data['surname']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        email = self.validated_data['email']
        is_medical_staff = self.validated_data['is_medical_staff']
        is_doctor = self.validated_data['is_doctor']
        is_final_authority = self.validated_data['is_final_authority']

        if password != password2:
            raise serializers.ValidationError(
                {
                    'error': 'passwords does not match'
                }
            )
        
        user = User(email = email, user_name = user_name, surname = surname, first_name = first_name, last_name= last_name,
                     is_medical_staff= is_medical_staff, is_doctor = is_doctor,
                       is_final_authority = is_final_authority, is_active = True)
        user.set_password(password)
        user.save()

        return user
    
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()