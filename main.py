class common:
	@staticmethod
	def view_products():
		print "List of products : "
		print "Id 	Name 	Group 	Sub-Group"
		print "-----------------------------------------"
		with open("products.txt") as f:
			for line in f:
				print line
		print "-----------------------------------------"

	@staticmethod
	def login():
		id=input("enter customer_id : ")
		password=input("enter customer_password : ")
		with open("customers.txt", "r+") as f:
			temp = f.read()
			f.seek(0)
			for line in temp.split('\n'):
				if(line == "" or line == " "):
					break
				line_tokens = line.split(' ')
				if(int(line_tokens[0]) == id and int(line_tokens[2]) == password ):
					return 1

			print "invalid login"
			return 0		

	@staticmethod
	def signup():
		id=input("enter customer_id : ")
		password=input("enter customer_password : ")
		name=raw_input("enter customer_name : ")
		with open("customers.txt", "a") as f:
			new_customer=str(id)+" "+str(name)+" "+str(password)+ "\n"
			f.write(new_customer)
			print "login again to continue"


class admin(common):
	def detail(self):
		flag=0
		admin_id=input("enter admin_id : ")
		admin_password=raw_input("enter password : ")

		with open("admin.txt","r+") as f:
			temp=f.read()
			for line in temp.split('\n'):
				line_tokens = line.split(' ')
				if int(line_tokens[0])==admin_id and line_tokens[1]==admin_password :
					print "welcome " + line_tokens[2]
					self.guide()
					flag=1

			if flag==0:
				print "invalid admin"

	def guide(self):
		print "1. view product"
		print "2. add product"
		print "3. delete product"
		print "4. modify product"
		print "5. make shipment"
		print "6. confirm delivery"

		choice=input("enter choice : ")

		if choice==1:
			self.view_products()
		if choice==2:
			self.add_products()
		if choice==3:
			self.delete_products()
		if choice==4:
			self.modify_products()
		if choice==5:
			self.make_shipment()				
		if choice==6:
			self.confirm_delivery()

	def add_products(self):
		p_id = input("Enter product id : ")
		p_name = raw_input("Enter product name : ")
		p_group = raw_input("Enter product group : ")
		p_sub_group = raw_input("Enter product sub group : ")
		f = open("products.txt", "a")
		f.write(str(p_id) + " " + p_name + " " + p_group + " " + p_sub_group + "\n")
		print "successfully added"

	def delete_products(self):
		with open("products.txt", "r+") as f:
			temp = f.read()
			p_id = input("Enter product id, which you want to delete : ")
			f.seek(0)
			for line in temp.split('\n'):
				if(line == "" or line == " "):
					break
				line_tokens = line.split(' ')
				if(int(line_tokens[0]) == p_id):
					print "this product gets successfully deleted : "
					print line
				else:
					f.write(line + "\n")
			f.truncate()
		print

	def modify_products(self):
		with open("products.txt", "r+") as f:
			temp = f.read()
			p_id = input("Enter product id, which you want to modify : ")
			f.seek(0)
			for line in temp.split('\n'):
				if(line == "" or line == " "):
					break
				line_tokens = line.split(' ')
				if(int(line_tokens[0]) == p_id):
					new_id = raw_input("Enter new id : ")
					new_name = raw_input("Enter new name : ")
					new_group = raw_input("Enter new group : ")
					new_subgroup = raw_input("Enter new subgroup : ")

					new_line = new_id + new_name + new_group + new_subgroup+ "\n"
					f.write(new_line)
					print "this product gets successfully modified : "
				else:
					f.write(line + "\n")
			f.truncate()
		print		

class customer(common):

	def __init__(self, c_id, c_name, c_address, c_phone_no):
		self.id = c_id
		self.name = c_name
		self.address = c_address
		self.phone_no = c_phone_no

	def guide(self):
		print "1. buy product"
		print "2. view product"
		print "3. make payment"
		print "4. add to cart"
		print "5. delete from cart"

		choice=input("enter ur choice customer : ")

		if choice==1:
			self.buy_products()
		if choice==2:
			common.view_products()
		if choice==3:
			self.make_payment()
		if choice==4:
			self.add_to_cart()
		if choice==5:
			self.delete_from_cart()				

	def buy_products(self):
		self.add_to_cart()	

	def add_to_cart(self):
		flag=0
		p_id = input("Enter the product id : ")
		with open("products.txt", "r+") as f:
			temp = f.read()
			for line in temp.split('\n'):
				if(line == "" or line == " "):
					break
				line_tokens = line.split(' ')
				if(int(line_tokens[0]) == p_id):
					f = open(str(self.id) + "_" + "cart.txt", "a")
					f.write(line + "\n")
					print "successfully added to cart"
					flag=1
					break

			if flag==0:
					print "failed to add product"	

	def make_payment(self):
		total=0
		shipments = open("shipments_pending.txt", "a")
		with open(str(self.id) + "_" + "cart.txt", "r+") as f:
			temp = f.read()
			for line in temp.split('\n'):
				if(line == "" or line == " "):
					break
				line_tokens = line.split(' ')
				total = total + int(line_tokens[4])
				shipments.write(str(self.id) + " " + line_tokens[0] + "\n")

		if(total == 0):
			print "Empty cart"
			return
		
		print "Total amount to be paid : ", total
		ch = raw_input("are you sure to make payment? (y/n) : ")
		if(ch == "y" or ch == "Y"):
			card_type = raw_input("Enter card type : ")
			card_no = raw_input("Enter card no : ")
			f = open("payments.txt", "a")
			f.write(str(self.id) + " " + self.name + " " + card_type + " " + card_no + "\n")

		open(str(self.id) + "_" + "cart.txt", 'w').close()				

	def delete_from_cart(self):
		with open(str(self.id) + "_" + "cart.txt", "r+") as f:
			temp = f.read()
			p_id = input("Enter product id, which you want to delete : ")
			f.seek(0)
			for line in temp.split('\n'):
				if(line == "" or line == " "):
					print "failed"
					break
				line_tokens = line.split(' ')
				if(int(line_tokens[0]) == p_id):
					print "successfully deleted from cart"
				else:
					f.write(line + "\n")
			f.truncate()
		print

class guest(common,customer):
	def __init__(self):
		print "1.view products"
		print "2.login"
		print "3.sign up"
		choice=input("enter ur choice mr guest: ")
		if choice==1:
			common.view_products()
		if choice==2:
			if common.login():
				customer_obj=customer()
				customer_obj.guide()
		if choice==3:
			common.signup()		
		
def main():
	while 1:
		print "1.admin"
		print "2.customer"
		print "3.guest"
		print "4. exit"
		choice=input("enter choice: ")

		if choice==1:
			admin_obj=admin()
			admin_obj.detail()

		if choice==2:
			flag=0
			customer_id=input("enter customer_id : ")
			customer_password=input("enter password : ")
			with open("customers.txt","r+") as f:
				temp=f.read()
				for line in temp.split('\n'):
					line_tokens = line.split(' ')
					if int(line_tokens[0])==customer_id and int(line_tokens[2])==customer_password :
						print "welcome " + line_tokens[1]
						customer_obj=customer(customer_id,line_tokens[1],line_tokens[3],line_tokens[4])
						customer_obj.guide()			
						flag=1
						break

				if flag==0:
					print "invalid customer"
			
			
		if choice==3:
			guest_obj=guest()

		if choice==4:
			exit()

if __name__ == '__main__':
	main()