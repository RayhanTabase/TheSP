from django.db import models
from user.models import User
from business.models import Business, Employee

class Room(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['business','customer'],
                name='unique room per user'
            )
        ]
    
    def __str__(self):
        return self.room_name

    def serialize(self):
        return {
            "customer": self.customer.username,
            "customer_image":self.customer.profile_picture.url,
            "room_name": self.room_name,
        }

class RoomMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    customer_created = models.BooleanField(default=False)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.customer_created:
            return self.room.customer.username
        return self.room.business.name

    def serialize(self):
        employee_name = None
        if self.employee:
            employee_name = self.employee.name
        return {
            "id":self.id,
            "message": self.message,
            "customer_created":self.customer_created,
            "employee":employee_name
        }

    # keep only 30 messages
    def delete_old_messages(self):
        all_messages = RoomMessage.objects.filter(room = self.room).order_by('id')
        length_messages = len(all_messages)
        if length_messages > 30:
            difference = length_messages - 30
            count = 0
            while count < difference:
                all_messages.first().delete()
                count += 1

    def save(self,*args,**kwargs):
        self.delete_old_messages()
        super().save(*args,**kwargs)


        


