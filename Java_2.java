package Paint;

public class Circle extends Figure implements Drawable{
    private final double radius;

    public Circle(Point point, double radius) {
        super(point);
        this.radius = radius;
    }

    public double area() {
        return Math.PI * radius * radius;
    }

    public double perimeter() {
        return 2 * Math.PI * radius;
    }

    public void draw() {
        System.out.println("Нарисован чёрный круг с координатами " + point.print());
    }

    public void draw(Color color) {
        System.out.println("Нарисована" + color + "круг с координатами " + point.print());
    }
}