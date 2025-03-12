function [dxdt, dydt, dxxdt2, dyydt2] = SplineDerivativeT(X,Y)
% SPLINEDERIVATIVES Find the fisrt and second derivatives of parametric
% plane curves with respect to t.

    t = cumtrapz(sqrt(gradient(X).^2 + gradient(Y).^2));

    fx = spline(t,X);
    fy = spline(t,Y);    

    d1fx = differentiate(fx);
    d1fy = differentiate(fy);
    d2fx = differentiate(d1fx);
    d2fy = differentiate(d1fy);

    ti = linspace(min(t),max(t),length(X));
    
    dxdt = ppval(d1fx,ti);    
    dydt = ppval(d1fy,ti);    
    dxxdt2 = ppval(d2fx,ti);    
    dyydt2 = ppval(d2fy,ti);
    
    dxdt(abs(dxdt)<1e-12) = 0;
    dydt(abs(dydt)<1e-12) = 0;
    dxxdt2(abs(dxxdt2)<1e-12) = 0;
    dyydt2(abs(dyydt2)<1e-12) = 0;

end

function ppdf = differentiate(ppf)
    % Spline Derivative
    ppdf = ppf;
    ppdf.order=ppdf.order-1;
    ppdf.coefs=ppdf.coefs(:,1:end-1).*(ppdf.order:-1:1);
end
