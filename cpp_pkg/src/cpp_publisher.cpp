#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class cpp_publisher: public rclcpp::Node {
	public:
		cpp_publisher(): Node("cpp_publisher"), ct(0) {
			publisher_ = this-> create_publisher<std_msgs::msg::String>("Topic" ,10);
			timer_ = this->create_wall_timer(
				std::chrono::seconds(1),
				std::bind(&cpp_publisher::timer_callback, this)
			);
			RCLCPP_INFO(this->get_logger(), "C++ PUBLISHER HAS STARTED");
			
		}
	private:
		void timer_callback() {
			auto msg = std_msgs::msg::String();
			msg.data = "C++ Publisher says: "+std::to_string(ct);
			publisher_->publish(msg);
			RCLCPP_INFO(this->get_logger(), "C++ Publisher published: %s", msg.data.c_str());
			ct++; 
		}
	rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
	rclcpp::TimerBase::SharedPtr timer_;
	int ct;
};

int main(int argc, char* argv[]) {
	rclcpp::init(argc, argv);
	rclcpp::spin(std::make_shared<cpp_publisher>());
	rclcpp::shutdown();
	return 0;
}
