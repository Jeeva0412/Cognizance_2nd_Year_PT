CREATE DATABASE flight_booking;
USE flight_booking;

CREATE TABLE available_flights (
    flight_id INT PRIMARY KEY AUTO_INCREMENT,
    flight_number VARCHAR(10),
    start_location VARCHAR(100),
    destination VARCHAR(100),
    flight_time TIME,
    price DECIMAL(10, 2)
);

INSERT INTO available_flights (flight_number, start_location, destination, flight_time, price)
VALUES
('FL123', 'Coimbatore', 'Chennai', '10:30:00', 3000.00),
('FL456', 'Goa', 'Mumbai', '14:15:00', 2000.00),
('FL789', 'Kochi', 'Delhi', '18:45:00', 2500.00);

CREATE TABLE booked_flights (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    flight_id INT,
    user_name VARCHAR(100),
    FOREIGN KEY (flight_id) REFERENCES available_flights(flight_id)
);

select * from available_flights;
select * from booked_flights;
